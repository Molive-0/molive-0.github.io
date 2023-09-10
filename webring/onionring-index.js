// onionring.js is made up of four files - onionring-widget.js, onionring-index.js (this one!), onionring-variables.js, and onionring.css
// it's licensed under the cooperative non-violent license (CNPL) v4+ (https://thufie.lain.haus/NPL.html)
// it was originally made by joey + mord of allium (蒜) house, last updated 2020-11-24

// === ONIONRING-INDEX ===
//this file builds the list of sites in the ring for displaying on your index page

var tag = document.getElementById('index');

sites = null;
var xhr = new XMLHttpRequest();
xhr.open('GET', 'https://mo.molive.live/webring/sites.json', true);
xhr.onload = function () {
  var status = xhr.status;
  if (status != 200) {
    tag.insertAdjacentHTML('afterbegin', `
  Failed to retrieve the sites json.
    `);
  } else {
    sites = JSON.parse(xhr.response);

    list = "";
    for (i = 0; i < sites.length; i++) {
      list += `<li><a href='${sites[i]}'>${sites[i]}</a></li>`;
    }

    tag.insertAdjacentHTML('afterbegin', `
<ul>
${list}
</ul>
`);
  }
}
xhr.send();
