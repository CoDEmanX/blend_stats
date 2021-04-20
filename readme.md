# Blend Stats for PHP

This is a small class/lib for PHP which lets users read file stats from blend files using blender through the command line interface for usage in blender related sites.

Blend Stats calls the Blender binary in your system path and then executes a python script which retrieves some basic stats from the passed file.

## Usage:

```php
<?php

// include the lib
include '/path/to/blend_stats.php';

// INSTANTIATE
// pass blend location immediately [*]
$bst = new BlendStats( '/path/to/blend/file.blend' );

// get the stats
$bst->get_stats();

// use the stats
foreach ( $bst->stats->scenes as $scene ) {
    echo $scene->name;
}

// Save to database? Save to File? Whatever you have to do.

?>
```


## Output Structure:

BlendStats::get_stats(); returns an object containing two arrays:

```php
<?php 
object(stdClass) {
    bad_images => array(
        // Contains paths to broken links
        )
    scenes => array(
        (int) 0 => object(stdClass) {
            name => 'Scene'
            objects_mesh => (int) 7
            polygons => (int) 5834
            polygons_modified => (int) 16539
            render_engine => 'CYCLES'
            triangles => (int) 32262
            verts => (int) 5754
            verts_modified => (int) 16675
        },
        (int) 1 => object(stdClass) {
            name => 'Scene.001'
            objects_mesh => (int) 0
            polygons => (int) 0
            polygons_modified => (int) 0
            render_engine => 'BLENDER_RENDER'
            triangles => (int) 0
            verts => (int) 0
            verts_modified => (int) 0
        }
    )
}

?>
```

## Notes:

You will need Blender installed on your website's server, this means that you'll need a dedicated server where you can install software on your own in order to use this lib effectively with PHP. (this lib might be modified in the future to make direct from PHP reads possible, but until then blender is a requirement/dependency).

This lib is rather slow, and you might need a lot of RAM on your server to run Blender from the cli as this lib requires it with acceptable performance.

[*] There's a second argument for the constructor with which the Blender binary call is passed; it defaults to `'blender'` and works just fine if you have Blender in your System PATH so this arg is optional. If for some reason you can't have Blender added to your System PATH var, then you should pass the path to your local Blender binary in the second parameter of the constructor; for example:

```php
<?php 

// ON WINDOWS:
$bst = new BlendStats('C:\\path\\to\\file.blend', 'C:\\path\\to\\blender\\blender');

// ON POSIX 
// normally in /usr/local/bin/blender 
// when compiled with WITH_PORTABLE=OFF
$bst = new BlendStats('/path/to/file.blend', '/usr/local/bin/blender');

?>
```

## License

This software is provided as is, without any warranty of any kind, if you mess up your server by using this library it's your responsibility to solve it. We do not provide support for this tool, and we will publish updates only when we need them.

You are welcome to contribute to this software with customizations and 
