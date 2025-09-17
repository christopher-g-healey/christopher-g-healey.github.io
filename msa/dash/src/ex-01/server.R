library( shiny )
shinyServer( function( input, output ) {   # Server logic for histogram
  output$distPlot <- renderPlot( {
    ggplot( data=chickwts, aes( x=weight ) ) + geom_histogram( binwidth=input$bins, colour="white", fill="lightblue", alpha=0.7 ) + scale_y_continuous( breaks=c( 1, 3, 5, 7, 9 ) ) + ggtitle( "Chicken Weight Distribution" )   } )
} ) 
