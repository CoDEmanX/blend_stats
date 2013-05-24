<?php

////////////
// CONFIG //
////////////

$blender_bin = '"C:\\Program Files\\Blender Foundation\\Blender\\blender"';

////////////


function parse_stats($input) {

    $start_marker = "---STATS---BEGIN---";
    $end_marker = "---STATS---END---";

    $start_pos = strpos($input, $start_marker);
    if ($start_pos === FALSE) return FALSE;

    $end_pos = strpos($input, $end_marker, $start_pos);
    //if ($end_pos === FALSE) $end_pos = strlen($input); // Maybe too unsafe
    if ($end_pos === FALSE) return FALSE; // Maybe too unsafe

    $start_pos += strlen($start_marker);

    $raw_stats = substr($input, $start_pos, $end_pos - strlen($input));

    $parsed_stats = json_decode($raw_stats, True);
    if ($parsed_stats === NULL) return FALSE;

    return($parsed_stats);

}

// display PHP fails
ini_set('display_errors', '1');

// will hold the command result
$result = "";

// do the blender call, store the output
//$result = shell_exec("blender -y -Y -b /var/www/demo/blenderphp/test.blend --python /var/www/demo/blenderphp/stats.py --verbose 2 ");
$result = shell_exec($blender_bin . ' -y -Y -b test.blend --python stats.py --verbose 2');
// CoDEmanX: what does "--verbose 2" do?

$parsed_stats = parse_stats($result);
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
<?php print_r($result); ?>
            </pre>

            </td><td>
                <pre id="right">
<?php
if ($parsed_stats === FALSE) echo("Couldn't parse stats, sorry.");
else print_r($parsed_stats);
?>
                </pre>
            </td>
        </tr>
    </table>
</body>
</html>
