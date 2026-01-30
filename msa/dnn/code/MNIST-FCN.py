#  Perform all required imports

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as datasets
import torchvision.transforms as transforms


class FCN( nn.Module ):

#  FCN model to convert image to digit, allow for multiple hidden layers

    def __init__( self ):
        super( FCN, self ).__init__()

        self.hidden0 = nn.Linear( 784, 128 )
        self.output = nn.Linear( 128, 10 )
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.LogSoftmax( dim=1 )

    #  End function __init__

    def forward( self, input ):
        hidden = self.hidden0( input )
        hidden = self.sigmoid( hidden )
        output = self.output( hidden )
        output = self.softmax( output )
        return output

    #  End function forward
#  End class FCN


def train( model, epoch, trainloader ):

#  Training function, use stochastic gradient descent to optimize

    criterion = nn.NLLLoss()
    optimizer = optim.SGD( model.parameters(), lr=0.003, momentum=0.9 )

    for e in range( 0, epoch ):
        running_loss = 0
        for images,labels in trainloader:
            #  Flatten images into a 784-long vector

            images = images.view( images.shape[ 0 ], -1 )

            optimizer.zero_grad()
            output = model( images )
            loss = criterion( output, labels )
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print( 'Epoch {}, training loss: {}'.\
          format( e, running_loss / len( trainloader ) ) )


#  Transform incoming greyscale data to a tensor, with a mean of 0.5 and a
#  stdev of 0.5 (NB: mean and stdev can take up to 3 arguments, to support
#  different mean/stdev for R,G,B image channels)

transform = transforms.Compose(
    [ transforms.ToTensor(),
      transforms.Normalize( (0.5,), (0.5,) )
    ]
)

#  Download datasets, if not already downloaded

trainset =\
  datasets.MNIST( './', download=True, train=True, transform=transform )
testset =\
  datasets.MNIST( './', download=True, train=False, transform=transform )

#  Process data in batches of 64 items, both for training and testing

trainloader =\
  torch.utils.data.DataLoader( trainset, batch_size=64, shuffle=True )
testloader =\
  torch.utils.data.DataLoader( testset, batch_size=64, shuffle=True )

model = FCN()

#  Put the model in training mode, train for 15 epochs

model.train()
train( model, 15, trainloader )

#  Evaluate the model on the 10000 test images

n = 0
correct = 0

model.eval()

for images,labels in valloader:
    for i in range( 0, len( labels ) ):
        img = images[ i ].view( 1, 784 )
        prob = model( img )

        #  Invert probabilities since they are natural log'd
        #  (LogSoftmax), then from a tensor to a list

        prob = torch.exp( prob )
        prob = prob[ 0 ].tolist()

        pred_label = prob.index( max( prob ) )
        true_label = labels[ i ].item()

        if true_label == pred_label:
            correct += 1
        n += 1

print( f'Images tested: {n}' )
print( f'Accuracy: {correct / n * 100.0:.2f}%' )