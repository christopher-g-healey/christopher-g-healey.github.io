#  Perform all required imports

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as datasets
import torchvision.transforms as transforms


class CNN( nn.Module ):
	def __init__( self ):
		super( CNN, self ).__init__()

		#  2D convolution, 1 input channel, 6 output channels, 4x4 kernel,
		#  stride of 1, 28x28 image will become a 25x25 result, b/c last
		#  4x4 kernel at right edge and bottom edge produces 1 result for 4
		#  cells, meaning image shrinks by 3 cells

		self.conv1 = nn.Conv2d( 1, 6, kernel_size=4, stride=1 )

		#  2D convolution, input size of 6(from previous convolution layer),
		#  output size of 16, this follows a MaxPool2d of size 2x2 with a
		#  padding of 1 to expand image to 26x26 from 25x25, this downsamples
		#  the image to 13x13

		self.conv2 = nn.Conv2d( 6, 16, kernel_size=2 )

		#  FCN section of CNN, result of second covolution is again MaxPool2d
		#  at 2x2 resolution with padding of 1, reduing image size from 14x14
		#  to 7x7 over the 16 ouptput filters

		self.fc1 = nn.Linear( 16 * 7 * 7, 120 )
		self.fc2 = nn.Linear( 120, 10 )

		self.pool = nn.MaxPool2d( 2, 2, padding=1 )
		self.relu = nn.ReLU()
		self.softmax = nn.LogSoftmax( dim=1 )

	def forward( self, input ):
		conv = self.conv1( input )
		conv = self.relu( conv )
		conv = self.pool( conv )
		conv = self.conv2( conv )
		conv = self.relu( conv )
		conv = self.pool( conv )

		conv = conv.view( -1, 16 * 7 * 7 )
		output = self.fc1( conv )
		output = self.relu( output )
		output = self.fc2( output )
		output = self.softmax( output )
		return output
	#  End function forward
#  End class CCN


def train( model, epoch, trainloader ):

#  Training function, use stochastic gradient descent to optimize

	criterion = nn.CrossEntropyLoss()
	optimizer = optim.SGD( model.parameters(), lr=0.003, momentum=0.9 )

	for e in range( 0, epoch ):
		running_loss = 0
		for images,labels in trainloader:
			#  Flatten images into a 784-long vector

			#images = images.view( images.shape[ 0 ], -1 )

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
	  transforms.Normalize( (0.1307,), (0.3081,) )
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

model = CNN()

#  Put the model in training mode, train for 15 epochs

model.train()
train( model, 15, trainloader )

#  Evaluate the model on the 10000 test images

n = 0
correct = 0

model.eval()

for images,labels in testloader:

	#  Use trained CNN to convert (batch of 64) images to class probabilities

	prob = model( images )

	#  Check all results against known class labels

	for i in range( 0, len( labels ) ):

		#  Invert probabilities since they are natural log'd
		#  (LogSoftmax), then from a tensor to a list

		p = torch.exp( prob[ i ] )
		p = p.tolist()

		pred_label = p.index( max( p ) )
		true_label = labels[ i ].item()

		if true_label == pred_label:
			correct += 1
		n += 1

print( f'Images tested: {n}' )
print( f'Accuracy: {correct / n * 100.0:.2f}%' )