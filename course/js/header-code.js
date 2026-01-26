function load_html( div_nm, html_nm )
  //  Load an external HTML file into a target HTML file using jQuery
  //
  //  div_nm:   ID of <div></div>
  //  html_nm:  Optional path and name of HTML file to load into div

{
  //  Ensure jQuery has loaded and evaluated before trying to use it

  setInterval( function() {
    if ( typeof $ != "undefined" ) {
      tg_div = $("#" + div_nm );
      $( tg_div ).load( html_nm );
    }
  }, 10 );
}


function eval_cmd( cmd )

  //  Evaluate various HTML header commands
  //
  //  cmd: Command string to evaluate
{
  var  elem;                          // DOM element
  var  end_script = '<' + '/script>'; // </script> built to not confuse DOM
  var  i;                             // Loop counter
  var  key;                           // Key for script elem property
  var  pos;                           // Position between key=value
  var  tok;                           // Input line split into tokens
  var  val;                           // Value for script elem property

  cmd = cmd.trim();
  if ( cmd.length == 0 ) {
    return elem;
  }

  if ( cmd.indexOf( '!--' ) != -1 ) {// Ignore comments
    return elem;
  }
  
  // Handle <script>javascript</script> commands
  
  if ( cmd.startsWith( "<script>" ) && cmd.endsWith( end_script ) ) {
    tok = cmd.split( /[<>]/ );
    for( i = 0; i < tok.length; i++ ) {
      if ( tok[ i ] == "script" ) {
        cmd = tok[ i + 1 ];
        break;
      }
    }
    
    elem = document.createElement( "script" );
    elem.text = cmd;
    document.head.appendChild( elem ).parentNode.removeChild( elem );
    return;
    
  // Handle <script javascript></script> commands
    
  // Strip </script> at end of command, if it exists

  } else if ( cmd.endsWith( end_script ) ) {
    cmd = cmd.substring( 0, cmd.length - end_script.length );
  }
  
  // Strip /> at end of command, if it exists

  if ( cmd.endsWith( " />" ) ) {
    cmd = cmd.substring( 0, cmd.length -3 ) + ">";
  }
  
  // Split command into tokens

  cmd = cmd.substring( 1, cmd.length - 2 );
  tok = cmd.split( /\s+/ );
  
  // Try to create element of specified type and make it run synchronously

  try {
    elem = document.createElement( tok[ 0 ] );
    try {
      elem.async = false;
    } catch {
      console.log( "eval_cmd(), no async in element type " + tok[ 0 ] );
    }
  } catch {
    console.log( 'eval_cmd(), cannot create element "' + tok[ 0 ] + '"' );
    return elem;
  }
  
  // For each key=val entry, set script element property

  for( i = 1; i < tok.length; i++ ) {
    pos = tok[ i ].indexOf( '=' );
    key = tok[ i ].substring( 0, pos );
    val = tok[ i ].substring( pos + 1, tok[ i ].length ).replace( /"/g, '' );
    elem[ key ] = val;
  }
  return elem;
}                                     // End function eval_command


/// Fetch current header HTML

var  http_root;												// HTTP root for JS course code
var  pos;															// Index into string
var  URL;															// Course header code HTML URL


//  Get HTTP root to directory containing course files

//  This code builds the location of header-code.html in a local filesystem, but
//  you cannot fetch() from file:///, only from https:// so we comment this out
//  and refer directly to the version of the file on github.io; this means we must
//  keep both the local and remote files sync'd properly...

//pos = document.currentScript.src.indexOf( "course/" );
//if ( pos == -1 ) {
//	console.log( 'header-code.js mainline(), cannot find "course/" in script name' );
//	throw new Error( 'header-code.js mainline(), cannot find "course/" in script name' );
//} else {
//	pos = pos + "course/".length;
//}

//http_root = document.currentScript.src.substring( 0, pos );
//URL = http_root + "html/header-code.html";

URL = "https://christopher-g-healey.github.io/course/html/header-code.html";

fetch( URL )
  .then( r => r.text() )

  // Process each command in header text

  .then( txt => {
    var  elem;                        // Current header element
    var  i;                           // Loop counter
    var  s;                           // Head of DOM's script list
    var  tok;                         // Current commands in header HTML

    txt = txt.trim().replace( /\r/g, '' );
    tok = txt.split( '\n' );
    
    // Evaluate each header line (command) in order

    for( i = 0; i < tok.length; i++ ) {
      elem = eval_cmd( tok[ i ] );
      if ( elem == undefined ) {      // No valid element returned, continue
        continue;
      }

      try {                           // Try to insert/evaluate script element
        s = document.getElementsByTagName( 'script' )[ 0 ];
        s.parentNode.insertBefore( elem, s );
      } catch {
        console.log( 'parse_header(), cannot evaluate "' + tok[ i ] + '"' );
      }
   }                                  // End process each comand in header
  } );                                // End fetch promise


