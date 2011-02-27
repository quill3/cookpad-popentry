#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datastores

query = datastores.Entries.gql('ORDER BY bukuma_count DESC')
fetched_entries = query.fetch(100)

print '''<html>
<head>
<title>クックパッド人気エントリー</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="css/html.css" />
<link rel="stylesheet" type="text/css" href="css/layout.css" />
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-568420-7']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
</head>
<body>
<div id="wrapper">
<div id="content">
<div id="header">
<h1>Cookpad Pop Entry</h1>
<h2><span class="highlight">クックパッドのレシピだけで人気エントリー</span></h2>
</div>
<div id="page">'''


for fetched_entry in fetched_entries:
  print '<span class="result"><a href="http://' + fetched_entry.entry_url.encode('utf-8')  + '" target="_blank" >' + fetched_entry.entry_title.encode('utf-8') +'</a></span>'
  print '<br>'
  print '<span class="users"><strong><a href="http://b.hatena.ne.jp/entry/' + fetched_entry.entry_url.encode('utf-8') + '" target="_blank">' + str(fetched_entry.bukuma_count) + ' users</a></strong></span>&nbsp;&nbsp;'
  print '<span class="timestamp">' + fetched_entry.hateb_added_date.strftime("%Y/%m/%d").encode('utf-8') + '</span>'
  print '<br><br>'

print '''<div class="footer">
<img src="http://code.google.com/appengine/images/appengine-noborder-120x30.gif" alt="Powered by Google App Engine" />
<br>
This service is created by <a href="http://d.hatena.ne.jp/quill3/" target="_blank" >quill3</a>.
<br>
(Here is <a href="http://github.com/quill3/cookpad-popentry" target="_blank" >source code</a> & <a href="http://d.hatena.ne.jp/quill3/archive?word=%2A%5B%A5%AF%A5%C3%A5%AF%A5%D1%A5%C3%A5%C9%BF%CD%B5%A4%A5%A8%A5%F3%A5%C8%A5%EA%A1%BC%5D" target="_blank" >development log</a>.)
</div>

</div>
</div>
</div>
</body>
</html>'''
