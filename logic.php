<?php

// display PHP fails
ini_set('display_errors', '1');

require "config.php";

function parse_stats($input) {

    global $start_marker, $end_marker;

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

function get_stats($blend_path) {

    global $blender_bin, $script_path;

    // do the blender call, store the output
    //$result = shell_exec("blender -y -Y -b /var/www/demo/blenderphp/test.blend --python /var/www/demo/blenderphp/stats.py --verbose 2 ");

    $result = shell_exec($blender_bin .' -y -Y -b '. $blend_path .' --python '. $script_path .' --verbose 2');
    // CoDEmanX: what does "--verbose 2" do?

    return($result);

}

?>