'use strict';
const e = require('./engine.js');
const cases = require('./expected.json');
let checks = 0, fails = 0;
function eq(a, b, label) {
  checks++;
  if (a !== b) { fails++; console.log('FAIL', label, 'engine:', a, 'oracle:', b); }
}
for (const c of cases) {
  let r, text;
  if (c.tool === 'inside') { r = e.insideMount(...c.args); text = e.renderInside(r); }
  else if (c.tool === 'slats') { r = e.slats(...c.args); text = e.renderSlats(r); }
  else { r = e.splitSpan(...c.args); text = e.renderSplit(r); }
  const keys = new Set([...Object.keys(r), ...Object.keys(c.expect)]);
  for (const k of keys) eq(JSON.stringify(r[k]), JSON.stringify(c.expect[k]), c.tool + ' ' + JSON.stringify(c.args) + ' .' + k);
  checks++;
  if (r.error) { if (text !== r.error) { fails++; console.log('FAIL render error passthrough', text); } }
  else if (typeof text !== 'string' || text.length < 5 || /error|undefined|NaN/.test(text)) { fails++; console.log('FAIL render text', text); }
}
// render-shape spot checks
eq(e.renderInside(e.insideMount(120.4,120.0,120.7,140,140.3,139.8,1)), 'Order 119 cm wide x 140.3 cm drop. square opening.', 'render inside default');
eq(e.renderSlats(e.slats(140,5,0.5)), '32 slats at 4.5 cm pitch cover 144.5 cm.', 'render slats default');
eq(e.renderSplit(e.splitSpan(300,180)), '2 blinds of 150 cm each - 2 blinds, even split.', 'render split default');
eq(e.renderSplit(e.splitSpan(150,180)), 'one blind does it at 150 cm.', 'render split single');
console.log(checks + ' checks, ' + fails + ' failures over ' + cases.length + ' cases');
process.exit(fails ? 1 : 0);
