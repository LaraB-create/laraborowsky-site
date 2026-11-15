// Contact form: sends through Web3Forms. Your email address is never in this page.
(function () {
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = document.getElementById('cf-status');
  var subject = document.getElementById('cf-subject');

  // Preselect the topic from the link, e.g. /contact?topic=key
  var params = new URLSearchParams(location.search);
  var map = { key: 'Request a key', hello: 'Just saying hello', other: 'Something else' };
  var wanted = map[params.get('topic')];
  if (!params.get('topic')) wanted = 'Just saying hello';
  var radios = form.querySelectorAll('input[name="topic"]');
  for (var i = 0; i < radios.length; i++) radios[i].checked = radios[i].value === wanted;

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    var key = form.querySelector('input[name="access_key"]').value;
    if (!key || key.indexOf('YOUR_') === 0) {
      status.textContent = 'This form isn’t connected yet. Please reach me on LinkedIn for now.';
      status.className = 'cf-status is-error';
      return;
    }
    var topic = form.querySelector('input[name="topic"]:checked');
    subject.value = 'laraborowsky.com: ' + (topic ? topic.value : 'new note');
    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    status.className = 'cf-status';
    status.textContent = 'Sending…';
    var data = Object.fromEntries(new FormData(form).entries());
    fetch(form.action, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(data)
    }).then(function (r) { return r.json(); }).then(function (res) {
      if (res && res.success) {
        form.reset();
        status.className = 'cf-status is-ok';
        status.textContent = 'Your note is on its way down the rabbit hole. I’ll write back soon.';
      } else {
        throw new Error('not sent');
      }
    }).catch(function () {
      status.className = 'cf-status is-error';
      status.textContent = 'Something went wrong and your note didn’t send. Please try again, or reach me on LinkedIn.';
    }).then(function () { btn.disabled = false; });
  });
})();
