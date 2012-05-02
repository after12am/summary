
doc = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>David A. Mellis: Fab Speakers</title>
<link rel="stylesheet" type="text/css" href="../style.css" />
</head>
    
<body>
<div id="all">
<div class="name"><a href="../index.html">David A. Mellis</a></div>
<div id="left">
<a href="http://www.flickr.com/photos/mellis/5425700847/"><img src="speakers384.jpg" /></a><br />
<a href="http://www.flickr.com/photos/mellis/5428760215/" title="Battery holder by dam, on Flickr"><img src="circuit124.jpg" class="smimg" width="124" height="93" alt="Battery holder" /></a><a href="http://www.flickr.com/photos/mellis/5428781643/" title="Speaker held tightly in place by dam, on Flickr"><img src="structure124.jpg" class="smimg" width="124" height="93" alt="Speaker held tightly in place" /></a><a href="http://www.flickr.com/photos/mellis/5610326493/" title="Derivate speaker design by dam, on Flickr"><img src="oval124.jpg" width="124" height="93" alt="Derivate speaker design"></a><br />
<p><i>Click an image see a larger version; <a href="http://www.flickr.com/photos/mellis/sets/72157625509466294/">more photos</a> are on Flickr.</i></p>
<h2>Variations</h2>
<a href="http://sarahpease.com/audioJar"><img class="smimg" src="jar.png" /></a><a href="http://moeller.io/owl-speakers.html"><img src="owl.jpg" /></a>
<p><i>Left: <a href="http://sarahpease.com/audioJar">audioJar</a> by Sarah Pease. Right: <a href="http://moeller.io/owl-speakers.html">owl speakers</a> by Jon Moeller.</i></p>
</div>
<div id="main">
<h1>Fab Speakers</h1>
<p>
These portable speakers are made from laser-cut wood, fabric, veneer, and electronics.  They are powered by three AAA batteries and compatible with any standard audio jack (e.g. on an iPhone, iPod, or laptop).
</p>
<p>
The speakers are an experiment in open-source hardware applied to consumer electronics.  By making their original design files freely available online, in a way that's easy for others to modify, I hope to encourage people to make and modify them.  In particular, I'd love to see changes or additions that I didn't think about and to have those changes shared publicly for others to use or continue to modify.  The speakers have been designed to be relatively simple and cheap in the hopes of facilitating their production by others.
</p>
<h2>Download</h2>
<p>
The speakers aren't yet available as a kit, but you can download the files and make them for yourself. 
</p>
<p>
<em>Structure:</em> <a href="fab-speakers.svg">fab-speakers.svg</a> (Inkscape), <a href="fab-speakers-structure.pdf">fab-speakers-structure.pdf</a><br />
<em>Eagle:</em> <a href="fab-speakers.brd">fab-speakers.brd</a>, <a href="fab-speakers.sch">fab-speakers.sch</a><br />
<em>Bill of Materials (BOM):</em> <a href="fab-speakers-bom.pdf">fab-speakers-bom.pdf</a><br />
<em>Schematic:</em> <a href="fab-speakers-schematic.pdf">fab-speakers-schematic.pdf</a><br />
<em>Gerbers:</em> <a href="fab-speakers-gerbers.zip">fab-speakers-gerbers.zip</a><br />
</p>
<h2>Materials</h2>
<p>
Use 6mm (1/4") plywood.  For the veneer, 1 9/16" edging backed with an iron-on adhesive is ideal (like <a href="http://www.rockler.com/product.cfm?page=5957">this one</a> from Rockler), but anything should work if you cut it to that width.  Pick whatever fabric you like.  For the electronic components, see the bill-of-materials above.  You'll also need two-conductor speaker wire, available at Radio Shack.  
</p>
<h2>Tools</h2>
<p>
The hardest requirement is access to a laser cutter.  Alternatively, you can get the parts cut from a service like <a href="http://ponoko.com/">Ponoko</a>.  You'll also need a soldering iron, wire strippers, a hot glue gun, and an iron (if using iron-on veneer edging) or wood glue (for other veneer).  
</p>
<h2>Make</h2>
<p>
For instructions on putting together the Fab Speakers, download the <a href="fab-speakers-instructions.pdf">instruction booklet (PDF)</a>.
</p>
<p>
Also, see these photo sets on Flickr: <a href="http://www.flickr.com/photos/mellis/sets/72157625881475939/detail/">soldering the electronic components</a> and <a href="http://www.flickr.com/photos/mellis/sets/72157626006874502/detail/">assembling the speakers</a>.
</p>
<h2>Wall-Mounted Variation</h2>
<p>
As shown in one of the photos to the left, there's also a wall-mounted, oval-shaped variation on the design.  It uses the same circuit board, but combines both speakers into a single unit that can hang on a nail or screw in the wall.  You'll want to replace the batteries with a 5V power supply (included in the bill of materials); just cut off the connector and solder the wires directly into the + and - holes for the battery holder.  You'll also want to omit the power switch and just solder together the holes where it would have gone.  
</p>
<p>
Download: <a href="fab-speakers-oval.svg">fab-speakers-oval.svg</a>
</p>
</div>
</div>
</body>
</html>
'''

def main():
    from extractor import extract
    print extract(doc)

if __name__ == '__main__': main()