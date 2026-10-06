// constants
// canvas fills the window width
function canvas_width() { return windowWidth }
// canvas fills the window height
function canvas_height() { return windowHeight }

const start_x = 100
const start_y = 100
const text_offset_y = 35 // shifts all text down
function end_x() { return canvas_width() - start_x }

// constants in pixels
const base_bar_width = 10

const top_bar_height = 30
var mid_bar_height = 90 // the x height; set from slider_xheight each frame
var bot_bar_height = 30 // the descender height; set from slider_descender each frame

const letter_kerning = 6 // base gap between letters
var kerning = 6          // gap between elements inside a letter, from slider_inner
const leading = 10
function line_height() { return mid_bar_height + top_bar_height + bot_bar_height + leading }

var bar_width = 10

// per-letter widths: each letter (by draw order) either holds at base width or
// eases to a small stretch, independently of the others
const hold_chance = 0.6   // chance a letter sits out (stays constant) when its rest ends
const min_wait = 30       // frames a letter rests before deciding again
const max_wait = 150
const min_dur = 60        // frames for one expand-and-contract cycle
const max_dur = 150
let measuring = false     // layout-only pass: nothing is drawn
let amp_scale = 1         // shrinks all stretching so the word fits the canvas
const color_narrow = '#e1ad01' // mustard: resting color in heatmap mode
const color_plain = '#000000'  // default type color in alphabet mode
const color_wide = [200, 30, 30]   // red
var letter_widths = []
var letter_idx = 0
var input_box;
var slider_noise;
var slider_height;
var slider_xheight;
var bg_picker;
var type_picker;
var type_row;
var slider_spacing;
var slider_inner;
var letter_gap = 0 // extra space after each letter, from slider_spacing
var slider_descender;
var mode_menu;

function is_original() { return mode_menu && mode_menu.value() == 'alphabet' }

var extra_v = 0 // vertical stretch of the letter currently being drawn

var width_label;
var height_row;

// a section heading inside the control panel
function add_section(panel, title) {
    createDiv(title).addClass('section').parent(panel)
}

// a labeled row inside the control panel; sliders also get a live value readout
function add_row(panel, label_text, control) {
    const row = createDiv('').addClass('row').parent(panel)
    const label = createSpan(label_text).addClass('label').parent(row)
    control.parent(row)
    if (control.elt.type == 'range') {
        const readout = createSpan(control.value()).addClass('readout').parent(row)
        control.readout = readout
        control.input(() => readout.html(control.value()))
    } else {
        control.addClass('wide')
    }
    return { row, label }
}

function set_visible(row, visible) {
    if (visible) row.removeClass('hidden')
    else row.addClass('hidden')
}

function setupUI() {
    textFont('Verdana');
    textSize(20);

    const panel = createDiv('').addClass('panel')

    add_section(panel, 'canvas')

    mode_menu = createSelect();
    mode_menu.option('heatmap expansion')
    mode_menu.option('alphabet')
    mode_menu.selected('alphabet')
    mode_menu.changed(update_ui)
    add_row(panel, 'mode', mode_menu)

    input_box = createInput("muriel cooper");
    add_row(panel, 'text', input_box)

    bg_picker = createColorPicker('#eae8e5');
    bg_picker.input(sync_page_background)
    add_row(panel, 'background', bg_picker)

    type_picker = createColorPicker(color_plain);
    type_row = add_row(panel, 'type color', type_picker).row

    add_section(panel, 'letterforms')

    slider_xheight = createSlider(20, 200, 90);
    add_row(panel, 'x height', slider_xheight)

    slider_descender = createSlider(0, 100, 30);
    add_row(panel, 'descender height', slider_descender)

    slider_inner = createSlider(0, 40, 6);
    add_row(panel, 'element spacing', slider_inner)

    slider_spacing = createSlider(0, 60, 0);
    add_row(panel, 'letter spacing', slider_spacing)

    add_section(panel, 'variation')

    slider_noise = createSlider(0, 37.5, 0, 0.5);
    width_label = add_row(panel, 'stretch', slider_noise).label

    slider_height = createSlider(0, 100, 0);
    height_row = add_row(panel, 'vertical stretch', slider_height).row

    update_ui()
    sync_page_background()
}

// keep the page behind the canvas the same color as the canvas
function sync_page_background() {
    document.body.style.background = bg_picker.value()
}

// only show the controls that matter for the current mode
function update_ui() {
    const original = is_original()
    width_label.html(original ? 'noise' : 'stretch')
    set_visible(type_row, original)
    set_visible(height_row, !original)
}

function setup() {
    createCanvas(canvas_width(), canvas_height());
    fill('black');
    noStroke()
    setupUI()
}

var coord_x = start_x
var coord_y = start_y

function windowResized() {
    resizeCanvas(canvas_width(), canvas_height())
}

function draw() {
    mid_bar_height = slider_xheight.value()
    bot_bar_height = slider_descender.value()
    letter_gap = slider_spacing.value()
    kerning = slider_inner.value()
    if (width != canvas_width() || height != canvas_height()) resizeCanvas(canvas_width(), canvas_height())
    if (is_original()) {
        draw_original()
    } else {
        draw_current()
    }
}

// the sketch as it was before the animated version: noisy per-bar widths,
// the full alphabet, and text wrapping from the top of the page
function draw_original() {
    letter_idx = 0
    extra_v = 0
    fill(type_picker.value())
    randomSeed(input_box.value().charCodeAt(0))
    background(bg_picker.value());

    // colophon in the top left corner, aligned with the menu's margin
    const margin = 24
    coord_x = margin
    coord_y = margin + top_bar_height + (mid_bar_height + extra_v) / 2
    draw_str("mitp")

    coord_x = start_x + 300 // clear of the colophon
    coord_y = start_y + text_offset_y
    draw_str(input_box.value())
    ln()

    alphabet = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]
    draw_chars_with_spaces(alphabet)
}

function draw_current() {
    randomSeed(input_box.value().charCodeAt(0))
    background(bg_picker.value());
    coord_y = canvas_height() / 2 + text_offset_y // line is vertically symmetric about coord_y

    const word = input_box.value()
    update_letters(word.replace(/ /g, '').length)

    // measure the word (no wrapping) at zero and full stretch. width is linear
    // in stretch, so if full stretch is too wide, scale it back to just fit.
    const avail = canvas_width() - 2 * start_x
    const w0 = measure(word, 0)
    const w1 = measure(word, 1)
    const f = w1 > avail ? max(0, (avail - w0) / (w1 - w0)) : 1
    const total = measure(word, f)

    // draw centered, so stretching grows outward from the middle
    measuring = false
    amp_scale = f
    letter_idx = 0
    coord_x = (canvas_width() - total) / 2
    draw_str(word, false)

    // hidden for now
    // draw_str("mitp")
    // ln()
    // alphabet = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]
    // draw_chars_with_spaces(alphabet)
    // draw_str("  hello world")
}

// width of str on one line at the given stretch scale; draws nothing
function measure(str, scale) {
    measuring = true
    amp_scale = scale
    letter_idx = 0
    coord_x = 0
    draw_str(str, false)
    measuring = false
    return coord_x - (str.endsWith(' ') ? kerning : letter_kerning + letter_gap) // drop trailing gap
}

function draw_str(str, wrap = true) {
    for (let idx = 0; idx < str.length; idx++) {
        if (str[idx] == ' ') {
            if (!is_original()) bar_width = base_bar_width
            step()
            step()
            step()
        } else {
            if (!is_original()) bar_width = next_letter_width()
            try {
                evalstr = str[idx]+"()"
                eval(evalstr)
            } catch (error) {
                console.log("unknown char", error);
            }
            coord_x += letter_gap + letter_kerning - kerning // last step() added kerning; keep the gap between letters independent
        }

        if (wrap && coord_x >= end_x() - 3*bar_width) {
            ln()
        }
    }
}

function draw_chars_with_spaces(cs) {
    for (const fn of cs) {
        if (!is_original()) bar_width = next_letter_width()
        fn()
        coord_x += letter_gap + letter_kerning - kerning
        if (fn != ln) {
            step()
        }
        if (coord_x >= end_x() - 3*bar_width) {
            ln()
        }
    }
}

// should handle offsets
function step() {
    coord_x += bar_width + kerning

    // original mode: re-roll each bar's width with the noise slider
    if (is_original()) {
        bar_width = slider_noise.value() > 0 ? base_bar_width + random(slider_noise.value()) : base_bar_width
    }
}

// advances every letter once per frame. each letter independently rests, then
// either sits out (stays constant) or runs one expand-and-contract cycle:
// pulse = (1 - cos(2*pi*progress)) / 2 goes 0 -> 1 -> 0 over the cycle.
// uses Math.random so the per-frame randomSeed doesn't freeze the choices.
function update_letters(count) {
    const max_w = slider_noise.value()
    const max_h = slider_height.value()
    for (let i = 0; i < count; i++) {
        let lw = letter_widths[i]
        if (!lw) {
            lw = letter_widths[i] = { active: false, progress: 0, dur: 1, amp_w: 0, amp_h: 0, strength: 0, pulse: 0, wait: Math.random() * max_wait }
        }
        if (lw.active) {
            lw.progress += 1 / lw.dur
            if (lw.progress >= 1) {
                lw.active = false
                lw.progress = 0
                lw.wait = min_wait + Math.random() * (max_wait - min_wait)
            }
        } else if (--lw.wait <= 0) {
            if (Math.random() < hold_chance) {
                lw.wait = min_wait + Math.random() * (max_wait - min_wait)
            } else {
                lw.active = true
                lw.dur = min_dur + Math.random() * (max_dur - min_dur)
                const rw = Math.random()
                const rh = Math.random()
                lw.amp_w = rw * max_w
                lw.amp_h = rh * max_h
                lw.strength = max(rw, rh)
            }
        }
        lw.pulse = lw.active ? (1 - cos(TWO_PI * lw.progress)) / 2 : 0
    }
}

// returns the width for the next letter, sets its vertical stretch (extra_v)
// and its fill: more stretched -> redder, less stretched -> mustard
function next_letter_width() {
    const lw = letter_widths[letter_idx++]
    extra_v = lw.pulse * lw.amp_h
    if (!measuring) {
        fill(lerpColor(color(color_narrow), color(...color_wide), lw.pulse * lw.strength))
    }
    return base_bar_width + lw.pulse * lw.amp_w * amp_scale
}

function ln() {
    coord_y += line_height()
    coord_x = start_x
}

// x is the leftmost coord, y is the vertically middle coord.
// vertical stretch (extra_v) grows symmetrically about y: the mid bar gets
// taller and the top/bottom bars and dots move outward by half of it.
function bar_mid() {
    top_left_x = coord_x
    top_left_y = coord_y - (mid_bar_height + extra_v)/2
    if (!measuring) rect(top_left_x, top_left_y, bar_width, mid_bar_height + extra_v)
}

function bar_top() {
    top_left_x = coord_x
    top_left_y = coord_y - (mid_bar_height + extra_v)/2 - top_bar_height
    if (!measuring) rect(top_left_x, top_left_y, bar_width, top_bar_height)
}

function bar_bot() {
    top_left_x = coord_x
    top_left_y = coord_y + (mid_bar_height + extra_v)/2
    if (!measuring) rect(top_left_x, top_left_y, bar_width, bot_bar_height)
}

function dot_mid() {
    top_left_x = coord_x
    top_left_y = coord_y - (mid_bar_height + extra_v)/2
    if (!measuring) rect(top_left_x, top_left_y, bar_width, bar_width)
}

function dot_bot() {
    top_left_x = coord_x
    top_left_y = coord_y + (mid_bar_height + extra_v)/2 - bar_width
    if (!measuring) rect(top_left_x, top_left_y, bar_width, bar_width)
}
