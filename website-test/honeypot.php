<?php
    $randomWait = 2.0 * mt_rand() / mt_getrandmax() + 1.0;
    //sleep($randomWait);
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>A simple AJAX website with jQuery</title>
<link rel="stylesheet" type="text/css" href="demo.css" />
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js"></script>
<script type="text/javascript" src="script.js"></script>

</head>

<body>
<a href="demo.php">ACCUEIL</a>

<div id="rounded">
<img src="img/top_bg.gif" alt="top" /><div id="main" class="container">
    <h1>A simple AJAX driven jQuery website</h1>
    <ul id="navigation">
    <li><a href="#page1">Page 1</a></li>
    <li><a href="#page2">Page 2</a></li>
    <li><a href="#page3">Page 3</a></li>
    <li><a href="#page4">Page 4</a></li>
    <li><img id="loading" src="img/ajax_load.gif" alt="loading" /></li>
    </ul>
    
    <div class="clear"></div>
    
    
    <div>
        <a href="http://localhost9"><img src="http://www.gif-maniac.com/gifs/50/49797.gif" height="1" width="1" border="0">localhost9</a>
    </div>
    <div id="localhost17">
        <a href="http://localhost17"><span style="display: block; position: relative; width: 2px; height: 2px; overflow: hidden;">localhost17</span></a>
    </div>
    <div>
        <div>
            <a href="http://localhost20"><img src="http://www.gif-maniac.com/gifs/50/49797.gif" height="1" width="1" border="0">localhost20</a>
        </div>
    </div>
    <div id="localhost21">
        <div>
            <a href="http://localhost21"><span style="display: block; position: relative; width: 2px; height: 2px; overflow: hidden;">localhost21</span></a>
        </div>
    </div>

    
    
    
    <div id="localhost19">
        <a style="display: block; position: relative; width: 2px; height: 2px; overflow: hidden;" href="http://localhost19">localhost19</a>
    </div>
    <div id="localhost11">
        <a href="http://localhost11"><span style="display: none;">localhost11</span></a>
    </div>
    <div>
        <a href="http://localhost15"><span><img style="height: 20px" src="http://www.gif-maniac.com/gifs/50/49797.gif"/></span></a>
    </div>
    <div>
        <a href="http://localhost16"><span style="display: none;"><img style="height: 20px" src="http://www.gif-maniac.com/gifs/50/49797.gif"/></span></a>
    </div>
    <div style="position: relative; top: 50px">
        <div style="position: absolute; height: 0;"><a style="position: absolute;" href="http://localhost12">localhost12</a></div>
    </div>
    <div style="position: relative;">
        <div style="position: relative;">
            <div style="position: absolute; top: 100px;">
                <a href="http://localhost13">localhost13</a>
            </div>
        </div>
    </div>
    <div style="position: relative;">
        <div style="position: relative;">
            <div style="position: absolute; left: -1000px;">
                <a href="http://localhost14">localhost14</a>
            </div>
        </div>
    </div>
    <div>
        <a href="http://localhost4/">localhost4</a>
    </div>

    <div>
        <a href="http://localhost18"><img src="http://www.gif-maniac.com/gifs/50/49797.gif" height="1" width="1" border="0"></a>
    </div>
    <div>
        <a href="http://localhost5" style="display: none">localhost5</a>
    </div>
    <div>
        <div style="display: none">
            <a href="http://localhost6">localhost6</a>
        </div>
    </div>
    <div>
        <a href="http://localhost10/">localhost10</a>
    </div>
    <div>
        <div style="position: absolute; left: -1000px; right: -500px;">
        <a href="http://localhost7">localhost7</a>
        </div>
    </div>
    <div>
        <a href="http://localhost8"><div style="height: 0px; width: 0px;"></div></a>
    </div>
    <div>
        <a href="http://localhost1/" style="margin-left: -1000px;">localhost1</a>
    </div>
    <div>
        <a href="http://localhost2/" style="position: absolute; left: -1000px;">localhost2</a>
    </div>
    <div>
        <a href="http://localhost3/" style="display: none;">localhost3</a>
    </div>
    

<div style="height: 3000px; position: relative;">test</div>
    <div>
        <a href="http://bottomlink/">bottomlink</a>
    </div>

    
    
    <div id="pageContent">
    MAIN
    <?php
        //echo $randomWait
    ?>
    </div>
    <div class="clear"></div>
<img src="img/bottom_bg.gif" alt="bottom" /></div>

<div align="center" class="demo">
this is a <a href="http://tutorialzine.com/" target="_blank">tutorialzine</a> demo</div>

</body>
</html>
