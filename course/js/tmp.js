/*- COURSE.JS --------------------------------------------------------------*/
/*  Javascript for all course web pages                                     */
/*                                                                          */
/*- Modification History: --------------------------------------------------*/
/*  When:       Who:                    Comments:                           */
/*                                                                          */
/*  27-Jul-24   Christopher G. Healey   Initial implementation from R's     */
/*                                      existing msa-R.js                   */
/*  31-Jul-24		Christopher G. Healey		Added function to calculate if it	  */
/*																			is day or night based on today's		*/
/*																			sunrise / sunset in Raleigh, NC			*/
/*                                      https://github.com/mourner/suncalc  */
/*  07-Aug-24   Christopher G. Healey   Added Opentip tooltip to light-dark */
/*                                      icon                                */
/*                                      https://www.opentip.org             */
/*  08-Aug-24   Christopher G. Healey   Added IP to geolocation lookup to   */
/*                                      set initial light or dark mode      */
/*                                      https://www.ipdata.co               */
/*--------------------------------------------------------------------------*/

//  Global variables

var  accordion_list = { };            // Dict of detail accordion IDs, val is..
                                      // ..currently expanded state (true/false)
var  canvas_dict = { };               // Dict of canvas element properties
var  code_dict = { };                 // Dict of code examples that can be copied
var  init = false;                    // Initialize code run flag
var  latitude = NaN;                  // Geolocation latitude from IP address
var  longitude = NaN;                 // Geolocation longitude from IP address


function active_accordion()

  //  Return IDs of active or open accordions
{
  var  i;                             // Loop counter
  var  id;                            // ID of current accordion
  var  key;                           // List of accordion IDs
  var  open_accordion = [ ];          // List of open accordions
    
    
  key = Object.keys( accordion_list );
  for( i = 0; i < key.length; i++ ) {
    id = key[ i ];

    if ( accordion_list[ id ] == true ) {
      open_accordion.push( id );
    }
  }

  return( open_accordion );
}                                     // End function active_accordion


function add_point( canvas, pos, col="red" )

  //  Add a point on the given canvas element
  //
  //  canvas:   ID of canvas element to draw into
  //  pos:      2D point position
  //  col:      Colour (default=red)
{
  var  c;                             // Canvas element
  var  ctx;                           // Canvas element context
  var  lr;				                    // LR corner of canvas, in (x,y) units
  var  ul;				                    // UL corner of canvas, in (x,y) units
  var  unit;				                  // Size of one unit in pixels
  var  x,y;				                    // X, Y-position on 2D grid


  c = document.getElementById( canvas );
  if ( c == null ) {			            // No such element?
    console.log( "add_point(), no canvas element with ID " + canvas );
    return;
  }

  //  Ensure proper endpoint lists

  if ( pos.length != 2 || pos.length != 2 ) {
    console.log( "add_point(), incorrect point" );
    console.log( "position: [" + pos + "]" );
    return;
  }

  //  Ensure canvas has been created with draw_line

  if ( !( canvas in canvas_dict ) ) {
    return;
  }

  ul = canvas_dict[ canvas ].ul;	    // Retrieve canvas properties
  lr = canvas_dict[ canvas ].lr;
  unit = canvas_dict[ canvas ].unit;

  ctx = c.getContext( "2d" );         //  Draw point

  x = pos[ 0 ] - ul[ 0 ];
  y = ul[ 1 ] - pos[ 1 ];

  ctx.beginPath();
  ctx.arc( x * unit, y * unit, 3, 0, 2 * Math.PI, false );
  ctx.fillStyle = col;
  ctx.fill();
  ctx.closePath();
}					                            // End function add_point


function add_line( canvas, beg, end, dash = [ ] )

  //  Add a line on the given canvas element from beg to end
  //
  //  canvas:   ID of canvas element to draw into
  //  beg,end:  2-element lists of 2D start and end points of line
  //  dash:     setLineDash pattern, default=solid
{
  var  c;				                      // Canvas element
  var  ctx;				                    // Canvas element context
  var  lr;				                    // LR corner of canvas, in (x,y) units
  var  ul;				                    // UL corner of canvas, in (x,y) units
  var  unit;				                  // Size of one unit in pixels
  var  x0,y0;				                  // X, Y-position on 2D grid
  var  x1,y1;				                  // X, Y-position on 2D grid


  c = document.getElementById( canvas );
  if ( c == null ) {			            // No such element?
    console.log( "add_line(), no canvas element with ID " + canvas );
    return;
  }

  //  Ensure proper endpoint lists

  if ( beg.length != 2 || end.length != 2 ) {
    console.log( "add_line(), incorrect endpoint lists" );
    console.log( "beg: [" + beg + "]" );
    console.log( "end: [" + end + "]" );
    return;
  }

  //  Ensure canvas has been created with draw_line

  if ( !( canvas in canvas_dict ) ) {
    return;
  }

  ul = canvas_dict[ canvas ].ul;	    // Retrieve canvas properties
  lr = canvas_dict[ canvas ].lr;
  unit = canvas_dict[ canvas ].unit;

  //  Draw line

  ctx = c.getContext( "2d" );

  if ( dash.length != 0 ) {		        // Non-default line dash pattern?
    try {
      ctx.setLineDash( dash );
    } catch {
      console.log( "draw_line(), invalid setLineDash option", dash );
    }
  }

  //  We first "white out" the line, then draw it in to remove any
  //  background that may already exist

  dash = [ [ ], dash ];
  style = [ "white", "red" ];

  for( i = 0; i < style.length; i++ ) {
    ctx.setLineDash( dash[ i ] );
    ctx.strokeStyle = style[ i ];

    ctx.beginPath();
    x0 = beg[ 0 ] - ul[ 0 ];
    y0 = ul[ 1 ] - beg[ 1 ];
    ctx.moveTo( x0 * unit, y0 * unit );
    x1 = end[ 0 ] - ul[ 0 ];
    y1 = ul[ 1 ] - end[ 1 ];
    ctx.lineTo( x1 * unit, y1 * unit );
    ctx.stroke();
    ctx.closePath();
  }

  ctx.beginPath();
  ctx.arc( x0 * unit, y0 * unit, 3, 0, 2 * Math.PI, false );
  ctx.fillStyle = "red";
  ctx.fill();
  ctx.closePath();

  ctx.beginPath();
  ctx.arc( x1 * unit, y1 * unit, 3, 0, 2 * Math.PI, false );
  ctx.fillStyle = "red";
  ctx.fill();
  ctx.closePath();
}					                            // End function add_line


function async_sleep( ms )

  //  Sleep w/out blocking using Promises
  //
  //  ms:  Milliseconds to sleep
{
  return new Promise( resolve => setTimeout( resolve, ms ) );
}					                            // End function async_sleep


function copy_code_new( txt )
{
  var  code = "";                     // Code from code block
  var  cur_ident;                     // Current indent width
  var  i;                             // Loop counter
  var  ident_n;                       // Number of spaces preceding line's code
  var  line;                          // Lines in code block
  var  pos;                           // Start of code in line
  var  tab_n = 0;                     // Current tab stop
  var  tab_w = null;                  // Tab width, in spaces
  

  //  Split text into non-blank lines

  line = txt.split( '\n' ).filter( function( tok ) {
    return tok.trim().length > 0;
  } );
  
  //  Search for first code line
  
  for( i = 0; i < line.length; i++ ) {
    if ( line[ i ][ 0 ] == "%" ) {    // Code line?
      break;
    }
  }

  if ( i == line.length ) {           // No code lines in code block?
    return;
  }

  // We assume first code line is "% ..." so after removing %, indent is 1 space

  cur_ident = 1;

  // Walk thru tokens, as indent size changes, assume new indent block

  for ( i = 0; i < line.length; i++ ) {
    if ( line[ i ][ 0 ] != "%" ) {    // Not a code line?
      continue;
    }
    
    //  Strip leading %, if all that's left is spaces, ignore line
    
    line[ i ] = line[ i ].substring( 1 );
    if ( line[ i ].trim().length == 0 ) {
      code = code + "<br>";
      continue;
    }

    ident_n = line[ i ].search( /\S/ );

    if ( ident_n != cur_ident ) {     // Indent level change?
      if ( tab_w == null ) {          // First indent change? Get tab width
        tab_w = ident_n - cur_ident;
      }
      
      if ( ident_n > cur_ident ) {    // Tab forward?
        tab_n += ( ident_n - cur_ident ) / tab_w;
      } else {                        // Tab backward
        tab_n -= ( cur_ident - ident_n ) / tab_w;
      }

      tab_n = ( tab_n < 0 ) ? 0 : tab_n;
      cur_ident = ident_n;
    }
    
    //  Add appropriate tab plus line to code block
    
    code = code + " ".repeat( tab_n * tab_w ) + line[ i ].trim() + "<br>";
  }
//code = code + "<br>";

  //  For some reason text() and html() return non-printable ASCII
  //  characters, so we need to scan code and remove them

  i = 0;
  while( i < code.length ) {
    if ( code.charCodeAt( i ) > 126 ) {
      code = code.substr( 0, i ) + code.substr( i + 1 );
    } else {
      i++;
    }
  }
  
  //  Convert spaces to &nbsp;
  
  code.replace( /\ /g, "&nbsp;" );
    
  //  It used to be you could just run this code directly and it would
  //  work, however Firefox decided this can only be run in response to
  //  a user event; to get around this, it's done as an event within a
  //  synchronous AJAX call (sigh)

  $.ajax( {
    method: "GET",
    async: false,
    url: "https://www.csc2.ncsu.edu/faculty/healey/msa/python/index.html",
    success: function( res ) {
      //  Start processing the copy code command by adding a temporary
      //  paragraph to the end of the document with the text to copy to
      //  the clipboard

      $("body").append( '<pre id="code-copy">' + code + "</pre>" );

      //  Obtain a reference to the temporarily appended code

      blk = document.getElementById( "code-copy" );
    
      //  Create a range object that holds the text of the code

      rng = document.createRange();
      rng.selectNodeContents( blk );

      //  Select the code within the range

      sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange( rng );

      try {
        rc = document.execCommand( 'copy' );
      } catch( e ) {
        rc = false;
      }

      if ( rc == false ) {
        console.log( "Could not copy text block" );
      }

      //  Remove temporary paragraph with code block

      $("#code-copy").remove();
    }
  } );
}                                     // End function copy_code_new


function copy_code( txt )

  //  Copy Python code in a code-div block
  //
  //  txt:  HTML text of div
{
  var  blk;                           // Copy block to copy
  var  code;                          // Python code from code block
  var  i;                             // Loop counter
  var  len;                           // Line length
  var  line;                          // Tokens in code block
  var  pos_dt;                        // Position of ...
  var  pos_gt;                        // Position of &gt;&gt;&gt;
  var  rc;                            // Return code from copy attempt
  var  rng;                           // Range object to hold code text
  var  sel;                           // Selection of text in range object
  var  tab_1 = "    ";                // Tab
  var  tab_2 = "        ";            // Two tabs
  var  tab_3 = "            ";        // Three tabs
  var  tab_4 = "                ";    // Four tabs
  var  tab_5 = "                    ";// Five tabs


  //  Remove newlines multiple spaces, and <em></em> in code block,
  //  then split into individual lines

  line = txt.replace( /\n/g, '' ).replace( /  +/g, ' ' );
  line = line.replace( /<em>/g, '' ).replace( /<\/em>/g, '' );
  line = line.split( '<br>' );

  //  Extract code lines from code block

  code = "";
  for( i = 0; i < line.length; i++ ) {

    //  Check for either "&gt;&gt;&gt;" or "..." to mark a code line

    pos_gt = line[ i ].indexOf( '&gt;&gt;&gt;' );
    pos_dt = line[ i ].indexOf( '...' );

    if ( pos_gt == -1 && pos_dt == -1 ) {
      continue;
    }

    if ( pos_gt != -1 ) {             // &gt;&gt;&gt; code block?
      code = code + line[ i ].substr( pos_gt + 12 ).trim() + "<br>";

    } else {                          // ... code block, handle tables
      len = line[ i ].length;
      end = len - 7;

      if ( line[ i ].indexOf( "tab-1" ) != -1 ) {
        code = code + tab_1 + line[ i ].substring( pos_dt + 24, end ) + "<br>";
      } else if ( line[ i ].indexOf( "tab-2" ) != -1 ) {
        code = code + tab_2 + line[ i ].substring( pos_dt + 24, end ) + "<br>";
      } else if ( line[ i ].indexOf( "tab-3" ) != -1 ) {
        code = code + tab_3 + line[ i ].substring( pos_dt + 24, end ) + "<br>";
      } else if ( line[ i ].indexOf( "tab-4" ) != -1 ) {
        code = code + tab_4 + line[ i ].substring( pos_dt + 24, end ) + "<br>";
      } else if ( line[ i ].indexOf( "tab-5" ) != -1 ) {
        code = code + tab_5 + line[ i ].substring( pos_dt + 24, end ) + "<br>";
      } else {
        code = code + line[ i ].substr( pos_dt + 4 ) + "<br>";
      }
    }
  }
  //code = code + "<br>";

  //  For some reason text() and html() return non-printable ASCII
  //  characters, so we need to scan code and remove them

  i = 0;
  while( i < code.length ) {
    if ( code.charCodeAt( i ) > 126 ) {
      code = code.substr( 0, i ) + code.substr( i + 1 );
    } else {
      i++;
    }
  }
  
  //  Convert spaces to &nbsp;
  
  code.replace( /\ /g, "&nbsp;" );
    
  //  It used to be you could just run this code directly and it would
  //  work, however Firefox decided this can only be run in response to
  //  a user event; to get around this, it's done as an event within a
  //  synchronous AJAX call (sigh)

  $.ajax( {
    method: "GET",
    async: false,
    url: "https://www.csc2.ncsu.edu/faculty/healey/msa/python/index.html",
    success: function( res ) {
      //  Start processing the copy code command

      //  Add a temporary paragraph to the end of the document with the
      //  text to copy to the clipboard

      $("body").append( '<pre id="code-copy">' + code + "</pre>" );

      //  Try to copy the code to the clipboard
      //  Obtain a reference to the temporarily appended code

      blk = document.getElementById( "code-copy" );
    
      //  Create a range object that holds the text of the Python code

      rng = document.createRange();
      rng.selectNodeContents( blk );

      //  Select the Python code within the range

      sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange( rng );

      try {
        rc = document.execCommand( 'copy' );
      } catch( e ) {
        rc = false;
      }

      if ( rc == false ) {
        console.log( "Could not copy text block" );
      }

      //  Remove temporary paragraph with Python code block

      $("#code-copy").remove();
    }
  } );
}                                     // End funtion copy_code


function draw_grid( ctx, ul, lr, w, h, unit )

  //  Draw a 2D Cartesian grid on the given canvas element
  //
  //  ctx:   Context of canvas element to draw into
  //  ul:    Upper-left corner of canvas, in (x,y) units
  //  lr:    Lower-right corner of canvas, in (x,y) units
  //  w,h:   Height and width of canvas in pixels
  //  unit:  Size of one unit in pixels
{
  var  i;                             // Loop counter
  var  x0,y0;                         // X, Y-position on 2D grid


  //  Horizontal grid lines

  ctx.setLineDash( [ 2, 4 ] );
  ctx.strokeStyle = "#b0b0b0";

  for( i = ul[ 1 ]; i >= lr[ 1 ]; i-- ) {
    ctx.beginPath();
    y0 = ul[ 1 ] - i;

    ctx.moveTo( 0, y0 * unit );
    ctx.lineTo( w, y0 * unit );
    ctx.stroke();

    ctx.closePath();
  }

  //  Vertical grid lines

  for( i = ul[ 0 ]; i <= lr[ 0 ]; i++ ) {
    x0 = i - ul[ 0 ];

    ctx.moveTo( x0 * unit, 0 );
    ctx.lineTo( x0 * unit, h );
    ctx.stroke();

    ctx.closePath();
  }

  ctx.setLineDash( [ ] );
  ctx.strokeStyle = "#000000";

  //  x=0 and y=0 basis grid lines, if they exist within the grid

  //  Draw x-axis, if it is on-screen

  if ( ul[ 1 ] >= 0 && lr[ 1 ] <= 0 ) {
    y0 = ul[ 1 ] * unit;

    ctx.beginPath();
    ctx.moveTo( 0, y0 );
    ctx.lineTo( w, y0 );
    ctx.stroke();
    ctx.closePath();

    arrow_w = unit / 6.0;
    arrow_h = unit / 4.0;

    ctx.fillStyle = "#000000";
    ctx.beginPath();
    ctx.moveTo( 0, y0 );
    ctx.lineTo( arrow_w, y0 - arrow_h );
    ctx.lineTo( arrow_w, y0 + arrow_h );
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo( w, y0 );
    ctx.lineTo( w - arrow_w, y0 - arrow_h );
    ctx.lineTo( w - arrow_w, y0 + arrow_h );
    ctx.closePath();
    ctx.fill();
  }

  //  Draw y-axis, if it is on-screen

  if ( ul[ 0 ] <= 0 && lr[ 0 ] >= 0 ) {
    x0 = -ul[ 0 ] * unit;

    ctx.beginPath();
    ctx.moveTo( x0, 0 );
    ctx.lineTo( x0, h );
    ctx.stroke();
    ctx.closePath();

    arrow_w = unit / 6.0;
    arrow_h = unit / 4.0;

    ctx.beginPath();
    ctx.moveTo( x0, 0 );
    ctx.lineTo( x0 + arrow_w, arrow_h );
    ctx.lineTo( x0 - arrow_w, arrow_h );
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo( x0, h );
    ctx.lineTo( x0 + arrow_w, h - arrow_h );
    ctx.lineTo( x0 - arrow_w, h - arrow_h );
    ctx.closePath();
    ctx.fill();
  }

  //  Canvas border

  ctx.strokeStyle = "#000000";
  ctx.beginPath();
  ctx.moveTo( 0, 0 );
  ctx.lineTo( w, 0 );
  ctx.lineTo( w, h );
  ctx.lineTo( 0, h );
  ctx.lineTo( 0, 0 );
  ctx.stroke();
  ctx.closePath();
}					// End function draw_grid


async function draw_line( canvas, ul, lr, beg, end, dash=[ ], unit=25 )

  //  Draw a line on the given canvas element from beg to end
  //
  //  canvas:   ID of canvas element to draw into
  //  ul:       Upper-left corner of canvas, in (x,y) units
  //  lr:       Lower-right corner of canvas, in (x,y) units
  //  beg,end:  2-element lists of 2D start and end points of line
  //  dash:     setLineDash pattern, default=solid
  //  unit:     Pixels per one unit on grid
{
  var  c;				                      // Canvas element
  var  d;				                      // Canvas dictionary entry
  var  ctx;				                    // Canvas element context
  var  h;				                      // Height of canvas, in pixels
  var  i;				                      // Loop counter
  var  w;				                      // Width of canvas, in pixels
  var  x0,y0;				                  // X, Y-position on 2D grid
  var  x1,y1;				//                X, Y-position on 2D grid


  c = document.getElementById( canvas );
  if ( c == null ) {			// No such element?
    console.log( "draw_line(), no canvas element with ID " + canvas );
    return;
  }

  //  Ensure proper canvas corners

  if ( ul.length != 2 || lr.length != 2 ||
       ul[ 0 ] >= lr[ 0 ] || ul[ 1 ] <= lr[ 1 ] ) {
    console.log( "draw_line(), incorrect canvas corners" );
    console.log( "UL: [" + ul + "]" );
    console.log( "LR: [" + lr + "]" );
    return;
  }

  //  Ensure proper endpoint lists

  if ( beg.length != 2 || end.length != 2 ) {
    console.log( "draw_line(), incorrect endpoint lists" );
    console.log( "beg: [" + beg + "]" );
    console.log( "end: [" + end + "]" );
    return;
  }

  //  Ensure valid units

  if ( unit < 5 ) {
    unit = 25;
  }

  //  Set canvas width and height in pixels

  w = ( lr[ 0 ] - ul[ 0 ] ) * unit;
  h = ( ul[ 1 ] - lr[ 1 ] ) * unit;

  c.width = w;
  c.height = h;

  //  Before we can use canvas_dict, the jQuery init code has to run to
  //  create the global variable; wait here if it hasn't happened yet

  while ( typeof init === "undefined" ) {
    await async_sleep( 250 );
  }

  //  Add canvas properties to canvas dictionary

  d = { 'ul': ul, 'lr': lr, 'unit': unit };
  canvas_dict[ canvas ] = d;

  //  Draw solid border around canvas, dashed grid inside canvas

  ctx = c.getContext( "2d" );
  draw_grid( ctx, ul, lr, w, h, unit );

  if ( dash.length != 0 ) {		// Non-default line dash pattern?
    try {
      ctx.setLineDash( dash );
    } catch {
      console.log( "draw_line(), invalid setLineDash option", dash );
    }
  }

  //  We first "white out" the line, then draw it in to remove any
  //  background that may already exist

  dash = [ [ ], dash ];
  style = [ "white", "red" ];

  for( i = 0; i < style.length; i++ ) {
    ctx.setLineDash( dash[ i ] );
    ctx.strokeStyle = style[ i ];

    ctx.beginPath();
    x0 = beg[ 0 ] - ul[ 0 ];
    y0 = ul[ 1 ] - beg[ 1 ];
    ctx.moveTo( x0 * unit, y0 * unit );
    x1 = end[ 0 ] - ul[ 0 ];
    y1 = ul[ 1 ] - end[ 1 ];
    ctx.lineTo( x1 * unit, y1 * unit );
    ctx.stroke();
    ctx.closePath();
  }

  ctx.beginPath();
  ctx.arc( x0 * unit, y0 * unit, 3, 0, 2 * Math.PI, false );
  ctx.fillStyle = "red";
  ctx.fill();
  ctx.closePath();

  ctx.beginPath();
  ctx.arc( x1 * unit, y1 * unit, 3, 0, 2 * Math.PI, false );
  ctx.fillStyle = "red";
  ctx.fill();
  ctx.closePath();
}					                            // End function draw_line


async function draw_point( canvas, ul, lr, pos, unit=25, col="red" )

  //  Draw a point on the given canvas element at pos
  //
  //  canvas:   ID of canvas element to draw into
  //  ul:       Upper-left corner of canvas, in (x,y) units
  //  lr:       Lower-right corner of canvas, in (x,y) units
  //  pos:      2D point position
  //  unit:     Pixels per one unit on grid
  //  col:      Colour (default=red)
{
  var  c;				                      // Canvas element
  var  d;				                      // Canvas dictionary entry
  var  ctx;				                    // Canvas element context
  var  h;				                      // Height of canvas, in pixels
  var  i;				                      // Loop counter
  var  w;				                      // Width of canvas, in pixels
  var  x,y;				                    // X, Y-position on 2D grid


  c = document.getElementById( canvas );
  if ( c == null ) {			            // No such element?
    console.log( "draw_line(), no canvas element with ID " + canvas );
    return;
  }

  //  Ensure proper canvas corners

  if ( ul.length != 2 || lr.length != 2 ||
       ul[ 0 ] >= lr[ 0 ] || ul[ 1 ] <= lr[ 1 ] ) {
    console.log( "draw_line(), incorrect canvas corners" );
    console.log( "UL: [" + ul + "]" );
    console.log( "LR: [" + lr + "]" );
    return;
  }

  //  Ensure proper endpoint lists

  if ( pos.length != 2 ) {
    console.log( "draw_point(), incorrect point position" );
    console.log( "position: [" + pos + "]" );
    return;
  }

  //  Ensure valid units

  if ( unit < 5 ) {
    unit = 25;
  }

  //  Set canvas width and height in pixels

  w = ( lr[ 0 ] - ul[ 0 ] ) * unit;
  h = ( ul[ 1 ] - lr[ 1 ] ) * unit;

  c.width = w;
  c.height = h;

  //  Before we can use canvas_dict, the jQuery init code has to run to
  //  create the global variable; wait here if it hasn't happened yet

  while ( typeof init === "undefined" ) {
    await async_sleep( 250 );
  }

  //  Add canvas properties to canvas dictionary

  d = { 'ul': ul, 'lr': lr, 'unit': unit };
  canvas_dict[ canvas ] = d;

  //  Draw solid border around canvas, dashed grid inside canvas

  ctx = c.getContext( "2d" );
  draw_grid( ctx, ul, lr, w, h, unit );

  x = pos[ 0 ] - ul[ 0 ];
  y = ul[ 1 ] - pos[ 1 ];

  ctx.beginPath();
  ctx.arc( x * unit, y * unit, 3, 0, 2 * Math.PI, false );
  ctx.fillStyle = col;
  ctx.fill();
  ctx.closePath();
}					                            // End function draw_point


function overlap_img( e, elem, w, h )

  //  Check if cursor overlaps copy code icon in code div
  //
  //  e:     Event info from mousemove
  //  elem:  Code div element
  //  w:     Width of copy code icon
  //  h:     Height of copy code icon
{
  var  LR = { };                      // Lower-right corner pos in elem coords
  var  LR_off = { };                  // Offset of cursor in elem
  var  off = { };                     // Offset of elem on page
  var  pad = { };                     // Padding of elem
    

  off.w = elem.innerWidth();          // Element offset/size info
  off.h = elem.innerHeight();
  off.pos = elem.offset();

  pad.w = off.w - elem.width();       // Element padding info
  pad.h = off.h - elem.height();
    
  //  Lower-right corner position in element-relative coordinates
    
  LR.x = off.pos.left + off.w - ( pad.w / 2.0 );
  LR.y = off.pos.top + off.h - ( pad.h / 2.0 );
    
  //  Offset of cursor from lower-right corner of element

  LR_off.x = LR.x - e.pageX;
  LR_off.y = LR.y - e.pageY;

  //  For whatever reason (0,0) for copy icon is at its center and baseline...

  if ( ( LR_off.x >= -w / 2.0 && LR_off.x <= w / 2.0 ) &&
       ( LR_off.y >= 0 && LR_off.y <= h ) ) {
    return true;
  } else {
    return false;
  }
}                                     // End function overlap_img


function sunrise_sunset( lat=NaN, lon=NaN )

  //  Return true if between sunrise and sunset, otherwise false
  //
  //  lat:  Latitude to check, default: NaN
  //  lon:  Longitude to check, default: NaN
{
  var  key = "824ca2555e8e9918163621e173faa62f9d5cb5b2d4258bc17df8da56";
                                      // IPData API key (https://www.ipdata.co)
    

  //  Copy any user-provided lat/lon to global latitude/longitude

  if ( !isNaN( lat ) && !isNaN( lon ) ) {
    latitude = lat;
    longitude = lon;
  }

  // No previous or user-provided lat/lon, do IP to geolocation lookup?

  if ( isNaN( latitude ) || isNaN( longitude ) ) {
    $.get("https://api.ipdata.co?api-key=" + key, function( resp ) {
      if ( ( "latitude" in resp ) && ( "longitude" in resp ) ) {
        latitude = resp.latitude;
        longitude = resp.longitude;
      } else {                        // Call failed, default to Raleigh NC lat/lon
        latitude = 35.7796;
        longitude = -78.6382;
      }
        
      set_theme( latitude, longitude );
    }, "json" );
      
  } else {                            // Already have lat/lon
    set_theme( latitude, longitude );
  }                                   // End if we have cached lat/lon
}                                     // End function sunrise_sunset


function set_theme( lat, lon )

  //  Set the web page theme to light or dark based on day or night at the
  //  given latitude and longitude
  //
  //  lat:  Latitude to check
  //  lon:  Longitude to check
{
  var  cur_dt_tm;                     // Current date and time
	var  sunrise_dt_tm;									// Today's sunrise
	var  sunset_dt_tm;									// Today's sunset
  var  sun_times;                     // Today's sun time information


  cur_dt_tm = new Date();
  sun_times = SunCalc.getTimes( cur_dt_tm, latitude, longitude );
      
  //  If sunrise can't be determined, default to Raleigh NC lat/lon
      
  if ( sun_times.sunrise == "Invalid Date" ) {
    latitude = 35.7796;
    longitude = -78.6382;

    sun_times = SunCalc.getTimes( cur_dt_tm, latitude, longitude );
  }

  sunrise_dt_tm = sun_times.sunrise;
  sunset_dt_tm = sun_times.sunset;
    
  //  If during day and theme is dark, switch to light; if during night and
  //  theme is light, switch to dark

  if ( cur_dt_tm > sunrise_dt_tm && cur_dt_tm < sunset_dt_tm ) {
  	if ( $("body").hasClass( "dark" ) ) {
      switch_theme();
    }
  }

  if ( cur_dt_tm <= sunrise_dt_tm || cur_dt_tm >= sunset_dt_tm ) {
    if ( $("body").hasClass( "light" ) ) {
      switch_theme();
    }
  }
}                                     // End function set_theme


function switch_theme()

  // Change theme from light to dark or vice-versa depending on current
  // theme
{
  var  banner_URL;                    // Page light & dark banner URLs
  var  class_ID;                      // Index into jQuery URL for theme change
  var  cur_tok;                       // Current URL token
  var  http_root =                    // Root of page URL
    "https://www.csc2.ncsu.edu/faculty/healey/";
  var  icon_src = [                   // Light & dark button icons
    "https://www.csc2.ncsu.edu/faculty/healey/course/figs/moon-icon-gradient.png",
    "https://www.csc2.ncsu.edu/faculty/healey/course/figs/sun-icon-gradient.png"
  ];
  var  jquery_URL = [                 // jQuery light & dark themes
    "https://code.jquery.com/ui/1.13.3/themes/excite-bike/jquery-ui.css",
    "https://code.jquery.com/ui/1.13.3/themes/dot-luv/jquery-ui.css"
  ];
  var  pos;                           // Position of start of URL root in URL
  var  URL_tok;                       // URL tokens following URL root


  //  Setup proper logo and inverted logo URLs based on current doc URL
    
  pos = window.location.href.indexOf( http_root );
  if ( pos == -1 ) {
    console.log( "switch_theme(), invalid URL root: " + window.location.href );
    return;
  }
    
  URL_tok = window.location.href.substring( pos + http_root.length );
  URL_tok = URL_tok.split( "/" );
    
  //  Remove spurious empty strings split likes to insert at end of array, or
  //  any *.html appended to URL path

  cur_tok = URL_tok[ URL_tok.length - 1 ];
  while( cur_tok.length == 0 || cur_tok.indexOf( ".html" ) != -1 ) {
    URL_tok.pop();
    cur_tok = URL_tok[ URL_tok.length - 1 ];
  }
    
  //  Build background-image URL
    
  banner_URL = "url(" + http_root + "";
  banner_URL = banner_URL + "course/figs/" + URL_tok[ URL_tok.length - 1 ] + "/";

  //  If in dark mode, switch to excite-bike light mode or dot-luv dark mode
  
  if ( $("body").hasClass( "dark" ) ) {
    class_ID = 0;
    banner_URL = banner_URL + "banner.png)";

    $("body").removeClass( "dark" );
    $("body").addClass( "light" );

  } else {
    class_ID = 1;
    banner_URL = banner_URL + "banner-inv.png)";

    $("body").removeClass( "light" );
    $("body").addClass( "dark" );
  }

  document.getElementById( "jquery-CSS" ).href = jquery_URL[ class_ID ];
  $("#light-dark").attr( "src", icon_src[ class_ID ] );
  $("#banner-img").css("background-image", banner_URL );
}                                     // End function switch_theme


function wait_for_init()

  //  Wait for DOM to process and jQuery to initialize global variables
{
  if ( typeof init !== "undefined" ) {
    return;
  } else {
    setTimeout( wait_for_init, 250 );
  }
}					                            // End function wait_for_init


$(document).ready( function() {
  var  div_id = [ ];                  // List of id:anchor's for nav bar
  var  elem;                          // List of all div's in HTML
  var  i;                             // Loop counter
  var  id;                            // Copy image ID
  var  code_IDs;                      // Code example IDs
  var  is_fixed;                      // Nav bar is pinned flag
  var  key;                           // Dict key
  var  nav;                           // Ref to nav bar's div
  var  nav_foot;                      // Ref to nav bar's bottom spacer
  var  nav_y;                         // Top of nav bar y-offset on page
  var  val;                           // Dict value
  var  w;                             // Reference to main window


  //  Search for div's with ID starting with "nav-"

  elem = document.getElementsByTagName( 'li' );

  //  For every "nav-" elem, parse "nav-NAME:ANCHOR" to setup a
  //  key-val pair in the div_id dictionary, used to jump to anchor
  //  when a id=key item is clicked in the nav bar

  for( i = 0; i < elem.length; i++ ) {
    if ( elem[ i ].id.match( /nav\-/ ) ) {

      //  Ensure format is key:val, print a warning if it isn't'
        
      if ( elem[ i ].id.indexOf( ":" ) != -1 ) {
        key = elem[ i ].id.split( ":" )[ 0 ];
        val = "#" + elem[ i ].id.split( ":" )[ 1 ];
        div_id.push( { "id": key, "div": val } );
      } else {
        console.log( 'Invalid "nav-" ID item: "' + elem[ i ].id + '"' );
        console.log( 'Format is: id="nav-NAME: ANCHOR-NAME"' );
      }
    }
  }

  //  Search for div's with ID ending in "-accordion", setup jQuery
  //  accordions to be closed on load/refresh

  elem = document.getElementsByTagName( 'div' );
  for( i = 0; i < elem.length; i++ ) {
    if ( elem[ i ].id.match( /\-accordion/ ) ) {
      id = elem[ i ].id;

      $("#" + id).accordion( {
        active: false,
        collapsible: true,
        autoHeight: false,
        heightStyle: "content",

        //  Catch accordion hidden/shown, update state accordingly
          
        activate: function( e, ui ) {
          var id;                     // ID of activated accordion

          id = e.target.id;
          if ( ui.newHeader.length > 0 ) {
            accordion_list[ id ] = true;
          } else {
            accordion_list[ id ] = false;
          }
        } 
      } );
      accordion_list[ id ] = false;
    }
  }

  //  This code tracks the navigation bar, if it scrolls past the top
  //  of the page, it's "floated" and pinned to the top of the page

  nav = $("#nav");                      // Grab nav bar div, footer div
  nav_foot = $("#nav-footer");

  nav_y = nav.offset().top;             // Get nav bar's top offset on page

  is_fixed = false;

  w = $(window);
  w.scroll( function() {
    var  fixed;                         // Nav bar should be fixed flag
    var  nav_h;                         // Nav bar height
    var  top;                           // Vert scrollbar's top offset on page

    top = w.scrollTop();                // Get vert sbar pos from top of page
    fixed = top > nav_y;                // Scrolled past nav bar's top on page?
    nav_h = $("#nav").height();         // Get nav bar's height

    if ( fixed && !is_fixed ) {         // Fix navbar in place?
      nav.css( {
        position: "fixed",
        top: 0,
        left: nav.offset().left,
        width: "98.5%"
      } );
      nav_foot.css( {
        position: "fixed",
        top: nav_h,
        left: nav.offset().left,
        width: "98.5%"
      } );

      is_fixed = true;

    } else if ( !fixed && is_fixed ) {  // Release fixed navbar?
      nav.css( {
        position: "static",
        width: "100%"
      } );
      nav_foot.css( {
        position: "static",
        width: "100%"
      } );

      is_fixed = false;
    }
  } );

  setTimeout(() => {
    w.scroll();                         // If page refresh, ensure nav bar shown
  }, 5000 );
    
  //  This code assigns tracking to mousemove and mouseclick, if user moves
  //  over a copy code icon, then clicks, the copy code function is invoked
  //  on the given code block

  $(".code-flex, .code-flex-pair, .code-flex-accordion, .code-flex-pair-accordion").
    mousemove( function( e ) {
      if ( overlap_img( e, $(this), 15, 20 ) ) {
        $(this).css( "cursor", "pointer" );
      } else if ( $(this).css( "cursor" ) == "pointer" ) {
        $(this).css( "cursor", "default" );
      }
  } );

  //  This code tracks interaction with the navigation bar, if user clicks on
  //  an item, scroll the page to the anchor that corresponds to that item

  $("#nav-list li").click( function() {
    var  id;                            //  ID of current "nav-" item in nav list

    //  Find div ID for whatever nav item user clicked

    for( i = 0; i < div_id.length; i++ ) {

        //  Invalid ID format, if so print warning and skip?
        
      if ( $(this).attr( "id" ).indexOf( ":" ) == -1 ) {

        continue;
      } else {
        id = $(this).attr( "id" ).split( ":" )[ 0 ];
        if ( id == div_id[ i ][ "id" ] ) {
          break;
        }
      }
    }

    if ( i >= div_id.length ) {   // Unknown nav item?
      console.log( "Unknown navigation ID " + $(this).attr( "id" ) );
    } else {

    //  Animate the top of the div to the top of the page, but offset
    //  by 25px to account for the navigation toolbar itself

      $("html, body").animate(
        { scrollTop: $(div_id[ i ][ "div" ]).position().top - 25 }, 'swing' );
    }
  } );

  //  This code assigns click handlers to all "Copy" images in code
  //  blocks, which will call the copy_code() function for the proper
  //  div on click

  code_IDs = document.querySelectorAll( "div[id^='code-']");
  for ( i = 0; i < code_IDs.length; i++ ) {
    id = "#" + code_IDs[ i ].id;
    if ( $(id).length == 0 ) {
      continue;
    }
    
    if ( id in Object.keys( code_dict ) ) {
      console.log( "mainline(), code ID duplicate: " + id );
    } else {
      code_dict[ id ] = true;
    }

    $(id).click( function( i ) {
      //copy_code( $("#" + this.id).html() );
      copy_code_new( $("#" + this.id).html() );
    } );
  }
    
  code_IDs = document.querySelectorAll( "div[id^='code-flex']");
  for ( i = 0; i < code_IDs.length; i++ ) {
    id = "#" + code_IDs[ i ].id;
    if ( $(id).length == 0 ) {
      continue;
    }
      
    $(id).click( function( i ) {
      copy_code( $("#" + this.id).html() );
    } );
  }

  // Handle clicks on the light-dark theme icon

  $("#light-dark").hover( function() {
    $(this).css( "cursor", "pointer" );
  } );

  $("#light-dark").click( function() {
    switch_theme();
  } );

  new Opentip( "#light-dark", "Switch light/dark theme", {style: "dark"} );

  // Switch body class to light or dark depending on time of day

  sunrise_sunset();
} );
