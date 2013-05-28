<?php

include "blend_stats.php";

$blend_path = "test/test.blend";

?>

<!DOCTYPE html>
<html>
<head>
    <title>.blend Statistics</title>
    <style type="text/css">

    pre {
        margin: 15px;
        padding: 15px;
        border: 1px solid gray;
    }

    td {
        vertical-align: top;
    }

    </style>
</head>
<body>
    <h2>BlendStats example</h2>
    <?php 
    $bst = new BlendStats( $blend_path );
    debug( $bst->get_stats() );
     ?>
</body>
</html>
