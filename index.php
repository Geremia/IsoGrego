<!DOCTYPE html>
<html>
<head>
  <meta name="generator" content="HTML Tidy for HTML5 for Linux version 5.8.0">
  <title>IsoGrego: Find Related Gregorian Chants</title><?php
  session_start();
  if (isset($_GET['n']))
        $n = $_SESSION['n'] = $_GET['n'];
  else
        if (isset($_SESSION['n']))
                $n = $_SESSION['n'];
  $file = fopen("max_id.txt", "r") or die('<font color="red">Unable to determine max GregoBase ID.</font>');
  $max_id = trim(fgets($file));
  $sync_time = date('Y-m-d', filemtime("GABCs/$maxid.gabc"));
  ?>
</head>
<body>
  <script type="text/javascript" src="/navbar.js"></script>
  <h1>IsoGrego</h1>
  <p>Find the top <i>n</i> Gregorian chants most similar to a given one, sorted by <a target="_blank" href="https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html">cosine TF-IDF similarity</a> of the <a target="_blank" href="https://gregobase.selapa.net/?page_id=53">GABC</a> files.</p>
  <p>Last sync with <a target="_blank" href="https://gregobase.selapa.net/">GregoBase</a>: 2024-05-13. Max GregoBase ID: <?php echo $max_id; ?>.</p>
  <p><small>🎩 tip: "<a target="_blank" href="https://stackoverflow.com/a/8897648/1429450">How to compute the similarity between two text documents?</a>" StackOverflow question. Originally inspired by "<a target="_blank" href="https://forum.musicasacra.com/forum/discussion/19917/examples-of-same-setting-different-texts/p1">examples of same setting, different texts?</a>" MusicaSacra forum thread. See <a target="_blank" href="https://github.com/Geremia/IsoGrego">the source code on GitHub</a>.</small></p>
  <form method="get">
    <p><label>Chant's <a target="_blank" href="https://gregobase.selapa.net/scores.php">GregoBase ID</a>: <input type="number" name="id" min="1" max="<?php echo $max_id; ?>" value="<?php $id = $_GET['id']; echo $id; ?>" onfocus="this.select();" autofocus=""></label> <small>See, e.g.: <a target="_blank" href="https://gregobase.selapa.net/source.php?id=3">1961 Solesmes <i>Liber Usualis</i></a></small></p>
    <p><label>Number of results (<i>n</i>): <input type="number" name="n" min="1" max="64" value="<?php echo $n; ?>"></label></p>
    <p><label><input type="submit" value="Find similar chants."></label></p>
  </form>
  <p>Click on the chant name to expand/contract the collapsible. Click the chant image to open it up in GregoBase. Click the 🔍 to find similarities to the given chant.</p>
  <ol start="0">
    <?php
    if (isset($id) and isset($n)) {
        if ($id < 0 or $id > $max_id)
                die('<font color="red">GregoBase ID must be >0 and ≤18138.</font>');
        else if ($n < 0 or $n > 64)
                die('<font color="red">Number of results must be >0 and ≤64.</font>');
        else {
                $file = fopen("shm.name.txt", "r") or die('<font color="red">Unable to open similarity matrix.</font>');
                $shm_name = trim(fgets($file));
                echo shell_exec('./TF-IDF.py ' . $shm_name . ' ' . $max_id . ' ' . ' ' . $id . ' ' . $n . ' 2>&1');
        }
    }
    ?>
  </ol>
</body>
</html>
