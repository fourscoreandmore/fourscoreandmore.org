/* Shared renderer for canonical score-review JSON. No edition data live here. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else { root.ScoreReport = api; api.start(); }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const escape = value => String(value ?? '').replace(/[&<>"']/g, character =>
    ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[character]));
  const own = (object, key) => Object.prototype.hasOwnProperty.call(object, key);
  const roman = number => {
    let value = number, result = '';
    for (const [amount, label] of [[1000,'M'],[900,'CM'],[500,'D'],[400,'CD'],[100,'C'],[90,'XC'],[50,'L'],[40,'XL'],[10,'X'],[9,'IX'],[5,'V'],[4,'IV'],[1,'I']]) {
      while (value >= amount) { result += label; value -= amount; }
    }
    return result;
  };
  function safeUrl(value) {
    const url = String(value ?? '').trim();
    if (/^(https?:|mailto:)/i.test(url)) return url;
    if (/^[a-z][a-z0-9+.-]*:/i.test(url) || url.startsWith('//') || /[\\\u0000-\u001f]/.test(url)) return '#';
    return url;
  }
  function localPath(value) {
    if (typeof value !== 'string' || !value || /[\\?#\u0000-\u001f]/.test(value) || value.startsWith('/') || value.includes(':')) return false;
    let decoded;
    try { decoded = decodeURIComponent(value); } catch { return false; }
    return !decoded.split('/').some(part => part === '..' || part === '.' || part === '');
  }
  function requireText(value, label) {
    if (typeof value !== 'string' || !value.trim()) throw new Error(label + ' must be non-empty text.');
  }
  function number(value, fallback = 0) {
    if (typeof value === 'number' && Number.isFinite(value)) return value;
    const fraction = typeof value === 'string' && value.match(/^(-?\d+)\/(\d+)$/);
    return fraction && Number(fraction[2]) ? Number(fraction[1]) / Number(fraction[2]) : fallback;
  }
  function compareRecords(a, b) {
    const physical = own(a, 'physical_start') && own(b, 'physical_start');
    return (physical ? a.physical_start - b.physical_start :
      number(a.movement) - number(b.movement) || number(a.section_order) - number(b.section_order) || a.measure_start - b.measure_start)
      || number(a.beat_start) - number(b.beat_start) || number(a.order) - number(b.order) || a.id.localeCompare(b.id);
  }
  function validate(bundle, expectedMode) {
    if (!bundle || typeof bundle !== 'object') throw new Error('Missing edition data.');
    const {metadata, report, policies} = bundle;
    if (!metadata || metadata.schema_version !== 2 || !report || report.schema_version !== 2) throw new Error('This renderer requires schema_version 2.');
    if (!['editorial', 'correction'].includes(report.document)) throw new Error('Unknown report audience.');
    if (expectedMode && report.document !== expectedMode) throw new Error('This page only accepts ' + expectedMode + ' data.');
    if (!/^sq\d+$/.test(metadata.sqid || '') || report.sqid !== metadata.sqid) throw new Error('Metadata and report must identify the same sqID.');
    for (const key of ['title', 'composer']) requireText(metadata[key], 'metadata.' + key);
    if (!localPath(metadata.score_file) || metadata.score_file.includes('/') || !metadata.score_file.endsWith('.mscx')) throw new Error('score_file must name the local native MSCX.');
    if (!policies || !policies.codes || typeof policies.codes !== 'object' || !policies.source) throw new Error('Missing shared policy reference data.');
    if (!/^https:\/\//.test(policies.source.url || '')) throw new Error('The policy source must be an HTTPS URL.');
    if (!Array.isArray(report.records)) throw new Error('records must be an array.');
    function references(refs, label) {
      if (!Array.isArray(refs || [])) throw new Error(label + ' must be an array of policy codes.');
      for (const code of refs || []) if (typeof code !== 'string' || !own(policies.codes, code)) throw new Error('Unknown policy reference: ' + code);
    }
    references(report.policy_refs, 'policy_refs');
    const ids = new Set();
    const records = report.records.map(record => {
      const row = {...record, images: (record.images || []).map(item => ({...item}))};
      if (!/^[A-Za-z][A-Za-z0-9_-]*$/.test(row.id || '') || ids.has(row.id)) throw new Error('Invalid or duplicate record ID: ' + row.id);
      ids.add(row.id);
      for (const key of ['title', 'location', 'part', 'type', 'summary']) requireText(row[key], row.id + '.' + key);
      if (typeof row.measure_start !== 'number' || !Number.isFinite(row.measure_start)) throw new Error(row.id + ' requires a numeric measure_start.');
      if (own(row, 'physical_start') && (!Number.isInteger(row.physical_start) || row.physical_start < 1)) throw new Error(row.id + ' has an invalid physical_start.');
      if (own(row, 'movement') && (!Number.isInteger(row.movement) || row.movement < 1 || row.movement > 999)) throw new Error(row.id + ' has an invalid movement.');
      if (own(row, 'movement_label') && !own(row, 'movement')) throw new Error(row.id + ' movement_label requires movement.');
      if (own(row, 'movement')) row.movement_label = row.movement_label || roman(row.movement);
      if (report.document === 'editorial' && row.status !== 'accepted') throw new Error('Public records must be accepted editorial choices.');
      if (report.document === 'correction' && (!['open', 'partial', 'repaired'].includes(row.status) || !['red', 'amber'].includes(row.severity))) throw new Error('Private records require separate status and red/amber severity.');
      if (row.body_markdown !== undefined && typeof row.body_markdown !== 'string') throw new Error(row.id + ' body_markdown must be text.');
      if (!Array.isArray(record.images || [])) throw new Error(row.id + ' images must be an array.');
      for (const item of row.images) {
        requireText(item.role, row.id + ' image role');
        requireText(item.caption, row.id + ' image caption');
        if (!localPath(item.path)) throw new Error(row.id + ' has an unsafe image path.');
        if (report.document === 'editorial' && (!item.path.startsWith('images/') || /^(before|after)(?:$|[_-])/.test(item.role))) throw new Error('Public records may only reference public editorial images.');
        if (report.document === 'correction' && !item.path.startsWith('images/')) throw new Error('Private images must remain within the private images folder.');
      }
      references(row.policy_refs, row.id + '.policy_refs');
      if (row.policy_review !== undefined) {
        const review = row.policy_review;
        if (!review || typeof review !== 'object' || Array.isArray(review)
          || !['covered', 'local_decision', 'clarification_needed', 'conflict'].includes(review.status)
          || typeof review.note !== 'string' || !Array.isArray(review.proposal_ids)) throw new Error(row.id + ' has an invalid policy_review.');
        if (review.proposal_ids.some(id => typeof id !== 'string' || !/^PROPOSAL-[A-Z0-9]+(?:-[A-Z0-9]+)*$/.test(id))
          || new Set(review.proposal_ids).size !== review.proposal_ids.length) throw new Error(row.id + ' has invalid proposal identifiers.');
      }
      return row;
    });
    for (const field of ['movement', 'physical_start']) {
      const count = records.filter(row => own(row, field)).length;
      if (count && count !== records.length) throw new Error('Include ' + field + ' on every record in this report.');
    }
    records.sort(compareRecords);
    return {metadata: {...metadata}, report: {...report, records}, policies};
  }
  function matches(record, filters = {}) {
    const query = String(filters.query || '').toLocaleLowerCase().trim();
    const searchable = [record.id, record.movement_label, record.section, record.location, record.source_measure_start,
      record.edition_measure_start, record.part, record.type, record.summary, record.body_markdown, ...(record.policy_refs || [])].join(' ').toLocaleLowerCase();
    return (!query || searchable.includes(query))
      && (!filters.type || filters.type === 'all' || record.type === filters.type)
      && (!filters.status || filters.status === 'all' || record.status === filters.status)
      && (!filters.severity || filters.severity === 'all' || record.severity === filters.severity)
      && (!filters.movement || filters.movement === 'all' || String(record.movement) === String(filters.movement));
  }
  function markdown(text, marked, figurePaths = []) {
    if (!text) return '';
    const renderer = new marked.Renderer();
    renderer.html = token => escape(typeof token === 'string' ? token : token.text);
    renderer.link = function (token) { return '<a href="' + escape(safeUrl(token.href)) + '">' + this.parser.parseInline(token.tokens) + '</a>'; };
    const figures = new Set(figurePaths);
    renderer.image = token => '<a href="' + escape(safeUrl(token.href)) + '" target="_blank" rel="noopener">'
      + (figures.has(token.href) ? escape(token.text || 'View excerpt') : '<img loading="lazy" src="' + escape(safeUrl(token.href)) + '" alt="' + escape(token.text) + '">') + '</a>';
    return marked.parse(text, {renderer, gfm: true, breaks: false});
  }
  function policyLinks(codes, policies) {
    return (codes || []).map(code => {
      const rule = policies.codes[code];
      return '<a class="policy-code" href="' + escape(safeUrl(rule.url || policies.source.url)) + '" title="' + escape(rule.label || code) + '">' + escape(code) + '</a>';
    }).join(' ');
  }
  function statusBadges(record) {
    const states = {open: 'Open', partial: 'Partial', repaired: 'Repaired'};
    return '<span class="status ' + escape(record.status) + '">' + states[record.status] + '</span>'
      + '<span class="severity ' + escape(record.severity) + '">' + (record.severity === 'red' ? 'Red' : 'Amber') + '</span>';
  }
  function policyNote(record, marked) {
    const review = record.policy_review;
    if (!review || (!review.note && !review.proposal_ids?.length)) return '';
    return '<aside class="policy-review"><strong>Policy reference review</strong>' + markdown(review.note || '', marked)
      + (review.proposal_ids?.length ? '<p class="proposal-reference">Proposed clarification: ' + review.proposal_ids.map(escape).join(', ') + '.</p>' : '') + '</aside>';
  }
  function render(input, marked, options = {}) {
    const bundle = validate(input, options.mode);
    const {metadata: meta, report, policies} = bundle;
    const records = report.records, privateMode = report.document === 'correction';
    const hasMovements = records.some(row => row.movement !== undefined);
    const reportPath = options.reportPath || (privateMode ? 'corrections.json' : 'editorial.json');
    const label = privateMode ? 'Private correction review' : 'Editorial notes';
    const movements = [...new Map(records.filter(row => row.movement !== undefined).map(row => [row.movement, row.movement_label])).entries()].sort((a,b) => a[0] - b[0]);
    const types = [...new Set(records.map(row => row.type))].sort();
    const optionsFor = pairs => pairs.map(([value, text]) => '<option value="' + escape(value) + '">' + escape(text) + '</option>').join('');
    const filter = (title, id, values, first) => '<label>' + title + '<select id="' + id + '"><option value="all">' + first + '</option>' + optionsFor(values) + '</select></label>';
    const rows = records.map(row => '<tr data-entry="' + row.id + '">'
      + (hasMovements ? '<td class="movement">' + escape(row.movement_label) + '</td>' : '')
      + '<td class="bar"><a href="#' + row.id + '">' + escape(row.location) + '</a></td><td>' + escape(row.part) + '</td>'
      + '<td><span class="type">' + escape(row.type) + '</span></td><td class="policy-cell">' + (policyLinks(row.policy_refs, policies) || '<span class="muted">Local decision</span>') + '</td>'
      + (privateMode ? '<td><div class="status-pair">' + statusBadges(row) + '</div></td>' : '')
      + '<td>' + escape(row.summary) + '</td><td><a class="view" href="#' + row.id + '">View <span class="sr-only">' + row.id + '</span><span aria-hidden="true">↗</span></a></td></tr>').join('');
    const roleLabels = {source:'Source', before:'Before repair', edition:'Edition', after:'After repair'};
    const imageLabel = role => roleLabels[role] || ((/^(source|before|edition|after)[_-]/.exec(role) || []).length ? roleLabels[role.split(/[_-]/)[0]] + ' continuation' : role);
    const cards = records.map(row => '<section id="' + row.id + '" class="entry" data-entry="' + row.id + '">'
      + '<div class="entry-kicker"><span>' + (hasMovements ? escape(row.movement_label) + '; ' : '') + (row.section ? escape(row.section) + '; ' : '') + escape(row.location) + '; ' + escape(row.part) + '</span>'
      + '<span class="type">' + escape(row.type) + '</span>' + (privateMode ? statusBadges(row) : '') + '</div>'
      + '<h2>' + escape(row.title.replace(new RegExp('^' + row.id + '\\s*[—–-]\\s*'), '')) + '</h2>'
      + '<p class="entry-policies"><span>References</span> ' + (policyLinks(row.policy_refs, policies) || 'Local editorial decision; no specific rule assigned.') + '</p>'
      + '<div class="entry-copy">' + markdown(row.body_markdown, marked, row.images.map(item => item.path)) + '</div>' + policyNote(row, marked)
      + '<div class="excerpts">' + row.images.map(item => '<figure><figcaption><strong>' + escape(imageLabel(item.role)) + '</strong> ' + escape(item.caption) + '</figcaption>'
        + '<a href="' + escape(item.path) + '" target="_blank" rel="noopener" aria-label="Open full-size excerpt: ' + escape(item.caption) + '"><img loading="lazy" src="' + escape(item.path) + '" alt="' + escape(item.caption) + '"></a></figure>').join('') + '</div>'
      + '<div class="entry-end"><span>' + escape(row.id) + '</span><a href="#overview">Back to list ↑</a></div></section>').join('');
    const metadataRows = [['Score ID', meta.sqid], ['IMSLP file number', meta.imslp_file_id], ['Source PDF', meta.source_filename],
      ['Printed edition', meta.source_bibliographic_description], ['Reprint', meta.source_reprint], ['Repository score path', meta.score_path],
      ['OpenScore baseline', meta.openscore_baseline || meta.openscore_common_ancestor_revision], ['OpenScore revision', meta.openscore_current_revision],
      ['MALerLab revision', meta.maler_revision], ['Source PDF SHA-256', meta.source_sha256]].filter(([,value]) => value !== undefined && value !== null)
      .map(([title, value]) => '<tr><th>' + escape(title) + '</th><td>' + escape(value) + '</td></tr>').join('');
    const catalogue = meta.catalogue_entry && typeof meta.catalogue_entry === 'object' ? '<h3>Catalogue entry</h3><pre>' + escape(JSON.stringify(meta.catalogue_entry, null, 2)) + '</pre>' : '';
    const stateCounts = privateMode ? ['open','partial','repaired'].map(state => records.filter(row => row.status === state).length + ' ' + state).join('; ') : records.length + ' editorial entries';
    return '<header class="site-header"><a class="wordmark" href="' + (privateMode ? '../index.html' : 'index.html') + '">OpenScore <span>String Quartets</span></a><span class="document-label ' + (privateMode ? 'private' : '') + '">' + label + '</span></header>'
      + '<main><section class="hero"><p class="eyebrow">' + escape(meta.composer) + '; ' + escape(meta.sqid) + '</p><h1>' + escape(meta.title) + '</h1>'
      + '<p class="subtitle">' + (privateMode ? 'Corrections and unresolved decisions for the editorial team.' : 'Editorial differences between the printed source and this edition.') + '</p>'
      + '<div class="edition-meta"><span>' + stateCounts + '</span>' + (meta.review_date ? '<span>Reviewed ' + escape(meta.review_date) + '</span>' : '')
      + '<span>' + escape(meta.edition_status || 'Working edition') + '</span>' + (meta.imslp_file_id ? '<span>IMSLP #' + escape(meta.imslp_file_id) + '</span>' : '') + '</div></section>'
      + '<section id="overview" class="overview"><div class="section-heading"><h2>' + (privateMode ? 'Correction register' : 'Editorial register') + '</h2><a href="' + escape(safeUrl(reportPath)) + '" download>JSON data ↗</a></div>'
      + '<div class="filters"><label class="search-label">Find a passage<input id="search" type="search" placeholder="Bar, instrument, phrase or policy code"></label>'
      + (hasMovements ? filter('Movement', 'movement-filter', movements, 'All movements') : '') + filter('Type', 'type-filter', types.map(type => [type,type]), 'All types')
      + (privateMode ? filter('Status', 'status-filter', [['open','Open'],['partial','Partial'],['repaired','Repaired']], 'All statuses') + filter('Severity', 'severity-filter', [['red','Red'],['amber','Amber']], 'All severities') : '')
      + '<span id="result-count" aria-live="polite">' + records.length + ' entries</span></div>'
      + '<div class="table-scroll" tabindex="0" role="region" aria-label="' + label + ' table"><table class="register"><thead><tr>' + (hasMovements ? '<th>Movement</th>' : '')
      + '<th>Bar(s)</th><th>Part</th><th>Type</th><th>Policy</th>' + (privateMode ? '<th>Status / severity</th>' : '') + '<th>' + (privateMode ? 'Review topic' : 'Editorial reading') + '</th><th><span class="sr-only">Details</span></th></tr></thead><tbody>' + rows + '</tbody></table></div>'
      + '<p id="no-results"' + (records.length ? ' hidden' : '') + '>' + (records.length ? 'No matching entries. Try another search or filter.' : 'No entries are recorded for this edition.') + '</p></section>'
      + '<section class="references"><h2>Transcription guidelines</h2><p><a href="' + escape(policies.source.url) + '">Notes for Transcribers</a>'
      + (report.policy_refs?.length ? '; ' + policyLinks(report.policy_refs, policies) : '') + '</p><p class="muted">Letter-number references link to the shared guidelines. Local explanations below describe their application to this edition.'
      + (policies.source.checked_on ? ' References checked ' + escape(policies.source.checked_on) + '.' : '') + '</p></section>'
      + (report.context_markdown ? '<details class="context"><summary>Review scope and source context</summary><div class="prose">' + markdown(report.context_markdown, marked) + '</div></details>' : '')
+ '<div class="entry-list">' + cards + '</div>'
+ (privateMode
  ? '<section class="provenance"><h2>Source and edition</h2>'
    + '<div class="score-links"><a href="../'
    + escape(meta.score_file)
    + '" download>Download native MuseScore score</a>'
    + '<a href="../index.html">Public editorial notes</a></div>'
    + '<details><summary>Bibliographic and version details</summary>'
    + '<div class="table-scroll"><table class="metadata">'
    + metadataRows + '</table></div>' + catalogue
    + (meta.catalogue_url
      ? '<p><a href="' + escape(safeUrl(meta.catalogue_url))
        + '">Repository catalogue</a></p>'
      : '')
    + '</details></section>'
  : '')
+ '<p class="credit">Transcription: OpenScore String Quartets'
+ (meta.transcriber ? ', ' + escape(meta.transcriber) : '')
+ (meta.score_licence ? ', ' + escape(meta.score_licence) : '')
+ '.</p></main>'
  }
  async function start() {
    if (typeof document === 'undefined') return;
    const host = document.getElementById('report'), notice = document.getElementById('load-notice');
    const config = document.body.dataset, mode = config.document;
    function announce(message) { notice.hidden = false; notice.textContent = message; }
    function show(input) {
      const bundle = validate(input, mode);
      host.innerHTML = render(bundle, window.marked, {mode, reportPath: config.source});
      document.title = bundle.metadata.title + '; ' + (mode === 'editorial' ? 'Editorial notes' : 'Private corrections');
      const controls = {query:'search', type:'type-filter', status:'status-filter', severity:'severity-filter', movement:'movement-filter'};
      const update = () => {
        const filters = Object.fromEntries(Object.entries(controls).map(([key,id]) => [key, document.getElementById(id)?.value || (key === 'query' ? '' : 'all')]));
        let count = 0;
        for (const record of bundle.report.records) {
          const visible = matches(record, filters);
          document.querySelectorAll('[data-entry="' + record.id + '"]').forEach(element => { element.hidden = !visible; });
          if (visible) count++;
        }
        document.getElementById('result-count').textContent = count + ' of ' + bundle.report.records.length + ' entries';
        document.getElementById('no-results').hidden = count !== 0;
      };
      for (const [key,id] of Object.entries(controls)) document.getElementById(id)?.addEventListener(key === 'query' ? 'input' : 'change', update);
      const anchor = location.hash.slice(1);
      if (anchor) requestAnimationFrame(() => document.getElementById(anchor)?.scrollIntoView());
      return bundle;
    }
    const embedded = document.getElementById('report-data');
    if (config.offline === 'true' && embedded) {
      try { show(JSON.parse(embedded.textContent)); announce('Standalone export. Edit the canonical JSON files and export again to refresh this copy.'); }
      catch (error) { announce('The standalone data could not be loaded: ' + error.message); host.innerHTML = '<main class="loading"><h1>Report unavailable</h1><p>Check the exported data before publishing.</p></main>'; }
      return;
    }
    if (location.protocol === 'file:') {
      host.innerHTML = '<main class="loading"><h1>Open this collection through its local server</h1><p>From the collection folder, run <code>python3 -m http.server 8000</code>, then open this page at <code>http://localhost:8000/</code>.</p><p>The maintained HTML reads its JSON files directly. Use the export command for a standalone copy that opens by double-clicking.</p></main>';
      announce('The browser cannot reliably load local JSON from a file URL. No stale embedded copy is being shown.');
      return;
    }
    try {
      const read = async path => { const response = await fetch(path, {cache:'no-store'}); if (!response.ok) throw new Error(path + ': HTTP ' + response.status); return response.json(); };
      const [metadata, report, policies] = await Promise.all([read(config.metadata), read(config.source), read(config.policies)]);
      show({metadata, report, policies});
    } catch (error) {
      announce('Could not load the current edition data: ' + error.message);
      host.innerHTML = '<main class="loading"><h1>Report unavailable</h1><p>Check the JSON files and their paths, then reload this page. No fallback copy has been substituted.</p></main>';
    }
  }
  return {validate, render, matches, compareRecords, escape, safeUrl, localPath, markdown, start};
});
