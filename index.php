<!DOCTYPE html>
<html>
<head>
    <title>Blend Stats</title>
    <style type="text/css">
        html {font-family: sans-serif;}
        pre {margin: 15px;padding: 15px;border: 1px solid gray;}
        td {vertical-align: top;}
    </style>
</head>
<body>
    <h2>BlendStats example</h2>
    <?php
    include "blend_stats.php";
    $bst = new BlendStats();
    debug( $bst->test() );
    ?>
</body>
</html>
