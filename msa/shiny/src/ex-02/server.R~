library( ggplot2 )
library( shiny )
shinyServer( function( input, output ) {   # Server logic for histogram
  output$distPlot <- renderPlot( {
    ggplot( data=chickwts, aes( x=weight ) ) + geom_histogram( binwidth=input$bins, colour="white", fill="lightblue", alpha=0.7 ) + scale_y_continuous( breaks=seq( 0, length( chickwts$weight ), by=2 ) ) + ggtitle( "Chicken Weight Distribution" )
  } )
} )
