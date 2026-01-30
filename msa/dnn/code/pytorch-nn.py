# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 11:01:56 2020

@author: healey
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


#  PyTorch DNN model class

class Model( nn.Module ):
    def __init__( self, embed_sz, n_num_col, n_out, layers, p=0.4 ):
        super().__init__()
        
        self.all_embeddings = nn.ModuleList( [ nn.Embedding( ni, nf ) for ni,nf in embed_sz ] )
        self.embedding_dropout = nn.Dropout( p )
        self.batch_norm_num = nn.BatchNorm1d( n_num_col )
        
        all_layers = [ ]
        n_cat_col = sum( ( nf for ni,nf in embed_sz ) )
        input_sz = n_cat_col + n_num_col
        
        for i in layers:
            all_layers.append( nn.Linear( input_sz, i ) )
            all_layers.append( nn.Sigmoid() )
            all_layers.append( nn.BatchNorm1d( i ) )
            all_layers.append( nn.Dropout( p ) )
            input_sz = i
            
        all_layers.append( nn.Linear( layers[ -1 ], n_out ) )
        self.layers = nn.Sequential( *all_layers )

        
    def forward( self, x_cat, x_num ):
        embeddings = [ ]
        for i,e in enumerate( self.all_embeddings ):
            embeddings.append( e( x_cat[ :, i ] ) )
        x = torch.cat( embeddings, 1 )
        x = self.embedding_dropout( x )
        
        x_num = self.batch_norm_num( x_num )
        x = torch.cat( [ x, x_num ], 1 )
        x = self.layers( x )
        
        return x

#  End PyTorch DNN model class
        

def build_tensors( dataset, cat_col, num_col, out_col ):
    """
    Build categorical, numeric, and target dataframes
    
    dataset:  (Wheat) dataset to query
    cat_col:  List of categorical column names
    num_col:  List of numeric column names
    out_col:  Target column name (one-value list)
    """
        
    code = [ ]
    
    #  For each categorical column, convert it to a numeric sequence, and
    #  save the value range
    
    for cat in cat_col:
        dataset[ cat ] = dataset[ cat ].astype( 'category' )
        code.append( dataset[ cat ].cat.codes.values )
        
    #  Stack each column's values, convert to integer, to form a "row"
    #  of converted categorical values, then convert them to a pytorch tensor
        
    cat_data = np.stack( code, 1 ).astype( int )
    cat_data = torch.tensor( cat_data, dtype=torch.int64 )
    
    #  Do the same stack/convert for numeric columns
    
    num_data = np.stack( [ dataset[ col ].values for col in num_col ], 1 )
    num_data = torch.tensor( num_data, dtype=torch.float )
    
    #  Flatten output column into a 1d tensor
    
    out_data = torch.tensor( dataset[ out_col ].values ).flatten()
    
    return cat_data,num_data,out_data

#  End function build_tensors
    

def build_train_test( n, cat_data, num_data, out_data ):
    """
    Build training and test datasets, 70/30 split, for categorical,
    numeric, and target data
    
    n:         Number of records
    cat_data:  Categorical data tensor
    num_data:  Numeric data tensor
    out_data:  Target data tensor
    """
    
    test_rec = int( n * 0.3 )
    
    cat_train = cat_data[ :n - test_rec ]
    cat_test = cat_data[ n - test_rec: n ]
    
    num_train = num_data[ :n - test_rec ]
    num_test = num_data[ n - test_rec: n ]
    
    out_train = out_data[ :n - test_rec ]
    out_test = out_data[ n - test_rec: n ]
    
    train_test = { }
    train_test[ "train" ] = { "cat": cat_train, "num": num_train, "out": out_train }
    train_test[ "test" ] = { "cat": cat_test, "num": num_test, "out": out_test }
    
    return train_test

#  End function build_train_test
    
    

def embed_cat( dataset, cat_col ):
    """
    Create embeddings for each categorical column
    
    dataset:  Dataset of raw categorical values
    cat_col:  List of categorical column names
    """
    
    cat_col_sz = [ len( dataset[ col ].cat.categories ) for col in cat_col ]
    cat_embed_sz = [
      ( col_sz, min( 50, ( col_sz + 1 ) // 2 ) ) for col_sz in cat_col_sz ]
    
    return cat_embed_sz

#  End function embed_cat
    

def print_stat( y_val, tg ):
    """
    Print test classification statistics
    
    y_val:  Y (target) values obtained from model
    tg:     Known target values
    """
    
    y_val = np.argmax( y_val, axis=1 )
    
    print( 'Confusion Matrix:' )
    print( confusion_matrix( tg, y_val ) )
    print( '\nClassification Report:' )
    print( classification_report( tg, y_val ) )
    print( 'Accuracy: ', accuracy_score( tg, y_val ) )
    
#  End function print_stat


def read_data( fname ):
    """
    Read dataset, return to caller as dataframe
    
    fname:  Input filename
    """
    
    dataset = pd.read_csv( fname )
    
    #  Randomly shuffle dataset rows
    
    dataset = dataset.sample( frac=1 )
    
    #  Final column is assumed to be target, check its range and make
    #  sure it's shifted to be 0-based
    
    min = dataset.min( axis=0 )[ -1 ]
    for i in range( 0, dataset.shape[ 0 ] ):
        dataset.iloc[ i, -1 ] -= min
        
    return dataset

#  End function read_data
    

def test( model, loss, test_dict ):
    """
    Test DNN model
    
    model:      Model to test
    loss:       Loss function
    test_dict:  Test data dictionary
    """
    
    with torch.no_grad():
        y_val = model( test_dict[ "cat" ], test_dict[ "num" ] )
        err = loss( y_val, test_dict[ "out" ] )
    
    print( f'Error: {err:.8f}\n' )
    return y_val
    
#  End function test
    

def train( model, epochs, loss, optimizer, train_dict ):    
    """
    Train DNN model
    
    model:       Model to train
    epochs:      Number of epochs to run
    loss:        Loss functino
    optimizer:   Optimizer function
    train_dict:  Training data dictionary
    """
    
    agg_loss = [ ]
    
    for i in range( 0, epochs ):
        i += 1
        
        y_pred = model( train_dict[ "cat" ], train_dict[ "num" ] )
        single_loss = loss( y_pred, train_dict[ "out" ] )
        agg_loss.append( single_loss )
        
        if i % 25 == 1:
            print( f'Epoch: {i:3}, loss: {single_loss.item():10.8f}' )
            
        optimizer.zero_grad()
        single_loss.backward()
        optimizer.step()
        
    print( f'Epoch: {i:3}, loss: {single_loss.item():10.8f}\n' )
    
#  End function train


#  Mainline
    
dataset = read_data( '/Users/healey/Downloads/wheat.csv' )

cat_col = [ 'Province' ]
num_col = [ 'Area', 'Perimiter', 'Compactness', 'Kernel-Length',
            'Kernel-Width', 'Asymmetry', 'Groove-Length' ]
out_col = [ 'Type' ]

cat_data,num_data,out_data = build_tensors( dataset, cat_col, num_col, out_col )
cat_embed_sz = embed_cat( dataset, cat_col )

train_test = build_train_test( dataset.shape[ 0 ], cat_data, num_data, out_data )

out_sz = np.unique( dataset[ out_col ].values ).size
model = Model( cat_embed_sz, num_data.shape[ 1 ], out_sz, [ 10 ], p=0.1 )

print( model )

loss_fn = nn.CrossEntropyLoss()
opt_fn = torch.optim.Adam( model.parameters(), lr=0.001 )

train( model, 1000, loss_fn, opt_fn, train_test[ "train" ] )

y_val = test( model, loss_fn, train_test[ "test" ] )
print_stat( y_val, train_test[ "test" ][ "out" ] )
