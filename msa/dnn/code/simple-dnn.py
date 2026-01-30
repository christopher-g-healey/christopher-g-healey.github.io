import numpy as np
import random

from csv import reader
from datetime import datetime
from math import exp

def activate( weight, inp ):
    """
    Compute the activation of a neuron, based on its incoming activations,
    its weights for each activation, and its bias
    
    weight:  List of weights for each neuron
    inp:     List of input activations
    """

    actv = weight[ -1 ]    #  Start with the bias
    
    for i in range( 0, len( weight ) - 1 ):
        actv = actv + ( weight[ i ] * inp[ i ] )
    return actv

#  End function activate
    

def backprop_err( network, expect ):
    """
    Backpropegate error from output layer back through hidden layer
    to input layer; error in the output layer is  the expected activation
    minus the derived activation times the slope of the derived activation;
    
    In the hidden layer, we accumulate for each neuron the weight on the
    link between neuron and output (or next layer) neuron times error in
    output neuron (weighted error) times the slope of the output
    
    network:  Result of forward propegation on network
    expect:   Expected output values
    """
    
    #  Walk backwards through the layers in the network
    
    for i in reversed( range( len( network ) ) ):
        layer = network[ i ]
        err = [ ]
        
        if i == len( network ) - 1:    #  Output layer
            for j in range( 0, len( layer ) ):    #  For all output neurons
                neuron = layer[ j ]
                err.append( expect[ j ] - neuron[ 'output' ] )
                
        else:    #  Hidden layer
            for j in range( 0, len( layer ) ):    #  For all hidden neurons
                err_val = 0.0
                
                #  Aggregate for all neurons in succeeding layer
                
                for neuron in network[ i + 1 ]:
                    err_val += ( neuron[ 'weights' ][ j ] * neuron[ 'delta' ] )
                    err.append( err_val )
                    
        #  Now add an error delta to each neuron's dict
                    
        for j in range( 0, len( layer ) ):
            neuron = layer[ j ]
            neuron[ 'delta' ] = err[ j ] * transfer_deriv( neuron[ 'output' ] )
                    

def forward_prop( network, row ):
    """
    Forward propegate by taking a row of data, considering it the initial
    input, passing it through the hidden layer in the network, and using
    those results to define the final output layer values
    
    network:  Hidden and output layer weights and biases
    row:      Row of starting input values
    """
    
    inp = row    #  Save initial input
    
    for layer in network:    #  For all hidden/output layers
        new_inp = [ ]    #  Activation results for current layer
        
        for neuron in layer:    #  For all neuros in current layer
            
            #  Compute activation for each neuron, save it as a dict
            #  output value in the neuron and append it to an output
            #  list
            
            actv = activate( neuron[ 'weights' ], inp )
            neuron[ 'output' ] = transfer( actv )
            new_inp.append( neuron[ 'output' ] )
            
        inp = new_inp    #  Output from this layer is input to next layer
        
    return inp  #  Return final input, which is output layer results

#  End function forward_prop
    

def init_network( n_inp, n_hidden_layer, n_hidden_node, n_out ):
    """
    Initialize a simple one-layer neural network
    
    n_inp:           Number of input values
    n_hidden_layer:  Number of hidden layers
    n_hidden_node:   Number of neurons in each hidden layer (list of vals)
    n_out:           Number of output categories
    """
    
    #  A network is a list of layers: input, 1 or more hidden, output
    
    network = [ ]
    
    #  Hidden layer, each neuron has n_inp links from input layer (fully
    #  connected), plus one more for bias

    for i in range( 0, n_hidden_layer ):
        hidden_layer = [ ]
        
        for j in range( 0, n_hidden_node[ i ] ):
        
            #  Create random weights from each input neuron, plus one for bias
            
            n_prev = n_inp + 1 if i == 0 else n_hidden_node[ i - 1 ] + 1
        
            neuron_wt = [ random.random() for k in range( 0, n_prev ) ]
            hidden_layer.append( { 'weights': neuron_wt } )
        
        network.append( hidden_layer )    #  Save hidden layer's weight lists
        
    #  Create an output layer simimlarly, but with n_out neurons
    
    output_layer = [ ]
    for i in range( 0, n_out ):
        neuron_wt = [ random.random() for j in range( 0, n_hidden + 1 ) ]
        output_layer.append( { 'weights': neuron_wt } )
        
    network.append( output_layer )    #  Save output layer's weight lists
    
    return network

#  End function init_network
    

def predict( network, row ):
    """
    For a trained network, predict the output value for a given input row
    
    network:  Trained network
    row:      Input row to predict
    """
    
    out = forward_prop( network, row )
    return out.index( max( out ) )

#  End function predict
    

def train_network( network, train, l_rate, decay, n_epoch, n_out ):
    """
    Train a network using stochastic gradient descent. Assume network
    is initialized, pass in a training set, define a learning rate that
    decreases as we train, and set the number of training epochs and
    number of outputs
    
    network:  Network to train
    train:    Training set
    l_rate:   Initial learning rate
    decay:    Learning rate decay
    n_epoch:  Number of epochs (iterations) to train
    n_out:    Number of outputs
    """
    
    init_l_rate = l_rate    #  Save initial learning rate
    
    for epoch in range( 0, n_epoch ):
        sum_err = 0
        
        for i,row in enumerate( train ):    #  For all training samples
            
            #  1. Forward propegate given training row thru network
            #  2. Set all expected values to 0, final value in training
            #     row defines location of expected output value of 1
            #  3. Backprop error through network to get error delta
            #  4. Update weights based on error delta
            #  5. Decay the learning rate
            
            out = forward_prop( network, row )    #  Step 1
            
            expect = [ 0 for i in range( 0, n_out ) ]    #  Expect output=0
            expect[ row[ -1 ] ] = 1    #  Reset one expect output=1
            
            #  Compute sum of error at each neuron, square to make it positive
            
            for i in range( 0, len( expect ) ):
                sum_err += ( expect[ i ] - out[ i ] ) ** 2
                
            backprop_err( network, expect )    #  Step 3
            update_wt( network, row, l_rate )    #  Step 4
            
            l_rate = init_l_rate * ( 1 / ( 1 + ( decay * i ) ) )
 
        if epoch % 50 == 0 or epoch == n_epoch - 1:  
            print( 'Epoch: %3d;  Error: %.3f' % ( epoch, sum_err ) )
            if epoch == n_epoch - 1:
                print( '\n' )
        
#  End function train_network
    

def transfer( actv ):
    """
    Transfer an activation result using the sigmoid function 1/(1+e^-x)
    
    actv:  Activation value to act as x in sigmoid
    """
    
    return 1.0 / ( 1.0 + exp( -actv ) )

#  End function transfer
    

def transfer_deriv( out ):
    """
    Transfer derivative of a neuron output, since we're using sigmoid we
    know derivative of sigmoid is  d/dx sigmoid(x)=sigmoid(x)(1-sigmod(x))
    
    out:  sigmoid(x)
    """
    
    return out * ( 1.0 - out )

#  End function transfer_deriv
    

def update_wt( network, row, l_rate ):
    """
    Update the weights for the network given an input row and the current
    learning rate
    
    network:  Network to update
    row:      Input row
    l_rate:   Learning rate
    """
    
    for i in range( 0, len( network ) ):    #  For all layers
        if i == 0:    #  Use original input for first layer
            inp = row[ :-1 ]    #  Get all input vals except for bias
        else:    #  Use previous layer's output as input
            inp = [ neuron[ 'output' ] for neuron in network[ i - 1 ] ]
            
        for neuron in network[ i ]:
            
            #  For each neuron, update its weight by adding learning rate
            #  times error from expected value times previous layer's input
            
            for j in range( len( inp ) ):
                neuron[ 'weights' ][ j ] += l_rate * neuron[ 'delta' ] * inp[ j ]
                
            #  Update bias weight, assume input for bias is 1.0
            
            neuron[ 'weights' ][ -1 ] += l_rate * neuron[ 'delta' ]
            
#  End function update_wt
            
            
###  File reading/parsing functions ###
            
def acc_metric( actual, predicted ):
    """
    Determine accuracy of actual versus predicted

    actual:     Actual, correct values
    predicted:  Predicted values
    """
    
    correct = 0
    for i in range( 0, len( actual ) ):
        correct = ( correct + 1 ) if actual[ i ] == predicted[ i ] else correct
    
    return correct / float( len( actual ) ) * 100.0

#  End function acc_metric
    

def cross_validation_split( dataset, n_folds ):
    """
    Split a dataset into folds for n-fold cross validation
    
    dataset:  Dataset to split
    n_folds:  Number of folds
    """
    
    dataset_split = [ ]
    dataset_copy = list( dataset )
    
    fold_size = int( len( dataset ) / n_folds )
    for i in range( 0, n_folds ):
        fold = [ ]
        while len( fold ) < fold_size:
            index = random.randrange( len( dataset_copy ) )
            fold.append( dataset_copy.pop( index ) )
        dataset_split.append( fold )
        
    return dataset_split

#  End function cross_validation_split
    
            
def dataset_col_minmax( dataset ):
    """
    Return minimum and maximum (float) values for each column in a dataset
    
    dataset:  Dataset to query
    """
    
    np_dset = np.array( dataset )
    stats = [ ]
    
    for i in range( 0, len( dataset[ 0 ] ) ):
        min_val = min( np_dset[ :, i ] )
        max_val = max( np_dset[ :, i ] )
        stats.append( [ min_val, max_val ] )
        
    return stats

#  End function dataset_col_minmax
    

def dataset_minmax( dataset ):
    """
    Find the minmum and maximum values for each column in a dataset
    
    dataset:  Dataset to query
    """
    
    min = np.amin( dataset, axis=0 )    #  List of mins over each column
    max = np.amax( dataset, axis=0 )    #  List of maxs over each column
    
    #  We want to concatenate corresponding min,max entries into a
    #  2-element list [min,max], then store all of those in a parent
    #  list; we must first split min and max into individual 1-element
    #  numpy arrays
    
    min_sp = np.split( min, len( min ) )
    max_sp = np.split( max, len( max ) )
    
    #  Now we can use numpy concatenate to get a list of 2-element
    #  [min,max] lists, one entry for each column in the original dataset
    
    minmax = np.concatenate( ( min_sp, max_sp), axis=1 )
    return minmax

#  End function dataset_minmax
    

def dataset_normalize( dataset, minmax ):
    """
    Normalize each column in a dataset to lie on the range 0..1
    
    dataset:  Dataset to normalize
    minimax:  [[min0,max0], [min1,max1], ...] min/max for each column
    """
    
    rng = [ ]    #  Calculate min/max range for each column
    for i in range( 0, len( minmax ) ):
        rng.append( minmax[ i ][ 1 ] - minmax[ i ][ 0 ] )
    
    for row in dataset:
        for i in range( len( row ) ):
            row[ i ] = ( row[ i ] - minmax[ i ][ 0 ] ) / rng[ i ]
            
#  End function dataset_normalize

            
def evaluate_alg( dataset, alg, n_folds, args ):
    """
    Evaluate algorithms using n_fold cross validation
    
    dataset:  Dataset to train/test from
    alg:      Algorithm to test
    n_fold:   Number of cross validation folds
    args:     Argument dict for algorithm: l_rate, epoch, hidden
    """
    
    #  Input are number of neurons in first hidden layer
    #  Outputs are unique target values, remember target value for each
    #  training sample is last row element
    
    #  Add one to every hidden layer node count to allow for bias
    
    for i in range( 0, len( arg[ "hidden" ] ) ):
        arg[ "hidden" ][ i ] += 1
    
    n_inp = len( dataset[ 0 ] ) - 1
    n_out = len( set( row[ -1 ] for row in dataset ) )
    net = init_network( n_inp, arg[ "layer" ], arg[ "hidden" ], n_out )
    
    folds = cross_validation_split( dataset, n_folds )
    scores = [ ]
    
    for i,fold in enumerate( folds ):
        print( 'Fold %d:' % ( i + 1 ) )
        
        #  Traininig set is everything except what's in fold
        
        train_set = list( folds )
        train_set.remove( fold )
        
        #  Use a list comprehension to floatten 2d list into 1d list of rows
        
        train_set = [ val for sub in train_set for val in sub ]
        
        #  Test set is all rows in current fold
        
        test_set = [ ]        
        for row in fold:
            row_cp = list( row )
            test_set.append( row_cp )

        train_network(
          net, train_set, arg[ "l_rate"], arg[ "decay" ], arg[ "epoch" ], n_out )
        
        correct = 0
        for row in test_set:
            p = predict( net, row )
            a = row[ -1 ]
            correct = ( correct + 1 ) if a == p else correct

        acc = correct / len( test_set ) * 100.0        
        scores.append( acc )
        
    return scores

#  End function evaluate_alg
    
            
def load_csv( fname ):
    """
    Load a CSV dataset
    
    fname:  Dataset filename
    """
    
    dataset = [ ]
    with open( fname, 'r' ) as file:
        csv_reader = reader( file )
        for row in csv_reader:
            if not row:
                continue
            dataset.append( row )
    
    file.close()
    
    dataset = dataset[ 1: ]    #  Remove header line
    return dataset

#  End function load_csv


def str_col_2_float( dataset, col ):
    """
    Convert a string column to float values
    
    dataset:  Dataset to query
    col:      Column to convert
    """
    
    for row in dataset:
        row[ col ] = float( row[ col ].strip() )
        
#  End function str_col_2_float
        
        
def str_col_2_int( dataset, col ):
    """
    Convert a string column to integer values
    
    dataset:  Dataset to query
    col:      Column to convert
    """
    
    str_val = [ row[ col ] for row in dataset ]
    uniq = set( str_val )
    
    lookup = { }
    for i,val in enumerate( uniq ):
        lookup[ val ] = i
        
    for row in dataset:
        row[ col ] = lookup[ row[ col ] ]
        
    return lookup

#  End function str_col_2_int


#  Mainline
    
random.seed( datetime.now() )    #  Seed random with current time

dataset = load_csv( 'C:/Users/healey/Downloads/wheat-seeds.csv' )
n_row = len( dataset )
n_col = len( dataset[ 0 ] )

#  Attributes are read as strings, convert to floats

for i in range( 0, len( dataset[ 0 ] ) - 1 ):
    str_col_2_float( dataset, i )

#  Target seed type read as string, convert to integer
    
str_col_2_int( dataset, len( dataset[ 0 ] ) - 1 )
    
#  Normalize columns in dataset
    
minmax = dataset_minmax( dataset )
dataset_normalize( dataset, minmax )
    
#  Numpy converts everything to float, so reset target values to int,
#  b/c we're doing a classification
    
str_col_2_int( dataset, len( dataset[ 0 ] ) - 1 )

#  Evaluate the prediction algorithms

n_folds = 5
l_rate = 0.1
l_decay = 0.01
n_epoch = 1000
n_layer = 1
n_hidden = 10

arg = {
  "l_rate": l_rate,
  "decay": l_decay,
  "epoch": n_epoch,
  "layer": n_layer,
  "hidden": [ n_hidden ] * n_layer
}

scores = evaluate_alg( dataset, backprop_err, n_folds, arg )

print( 'Scores:  ', end='' )
for i in range( 0, len( scores ) ):
    print( '%.3f%%; ' % scores[ i ], end='' )
print( '\n' )

print( 'Mean Accuracy: %.3f%%' % ( sum( scores ) / float( len( scores ) ) ) )