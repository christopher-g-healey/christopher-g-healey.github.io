library( ggplot2 )
library( shiny )
shinyServer( function( input, output ) {
  df <- reactive( {
    return( subset( iris, Species == input$species ) )
  } )
  output$distPlot <- renderPlot( {
    if ( input$points == "outlier" ) {
      ggplot( data=df(), aes( x=Species, y=Sepal.Width ) ) + geom_boxplot( color="black", fill="palegreen", outlier.color="red", outlier.shape=1, coef=input$iqr ) + ggtitle( "Sepal Width Boxplot" )
    } else {
      ggplot( data=df(), aes( x=Species, y=Sepal.Width ) ) + geom_boxplot( lwd = 1, color="black", fill="palegreen", coef=input$iqr ) + geom_dotplot( aes( fill=Species ), binaxis="y", stackdir="center", method="histodot", binwidth=0.1, dotsize=0.75 ) + ggtitle( "Sepal Width Boxplot" ) + guides( fill=FALSE )
    }
  } )
} )
