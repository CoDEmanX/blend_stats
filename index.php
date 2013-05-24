<?php

require "logic.php";

$blend_path = "test/test.blend";

$raw_stats = get_stats($blend_path);
$stats = parse_stats($raw_stats);

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
    <table>
        <tr>
            <td>


                <pre id="left">
<?php
                    print_r($raw_stats);
?>
                </pre>

            </td>
            <td>
                <pre id="right">
<?php
                    if ($stats === FALSE) {
                        echo("Couldn't parse stats, sorry.");
                    } else {
                       print_r($stats);
                    }
?>
                </pre>
            </td>
        </tr>
    </table>
</body>
</html>
