from sklearn import datasets
from tendupden import WGANGP
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as mp

def normalize(dataset, mean, std):
    """
    Normalises the dataset by mean and standard deviation
    """
    mid = dataset - mean
    new_data = mid / std
    return new_data


def unnormalize(dataset, mean, std):
    """
    Reverts the normalised dataset to original format
    """
    df = pd.DataFrame(dataset)
    mid = df * std
    original = mid + mean
    return original

def get_norm(data):
    """
    Provides the mean and standard deviation for the dataset so it can be normalised.
    """
    mean = data.mean()
    std = data.std()
    data = normalize(data, mean, std)
    return data, mean, std

def show_loss_progress(loss_discriminator, loss_generator, filepath, extention=".pdf"):
    """
    This plots and saves the progress of the Loss function over time
    """
    mp.plot(loss_discriminator)
    mp.savefig(filepath + "_loss_progress_discriminator" + extention)
    mp.plot(loss_generator)
    mp.savefig(filepath + "_loss_progress_generator" + extention)
    mp.clf()


def dagplot(x,y,i):
    fake = pd.DataFrame(x)
    real = pd.DataFrame(y)
    fake['dataset'] = ['fake']*len(x)
    real['dataset'] = ['real']*len(y)
    result = pd.concat([real, fake])
    sns.pairplot(result,hue='dataset')
    mp.savefig(str(i) + "_compare.pdf")
    mp.clf()

batch = 100
iris = datasets.load_iris()
no_field = len(iris.data[1])
mygan = WGANGP(optimiser = 'adam'
        , input_dim = no_field
        , noise_size = batch
        , batch_size = batch
        , number_of_layers = 5
        , lambdas = 10
        , learning_rate = 0.008
        )

norm_data, mean, standard = get_norm(iris.data)
mygan.critic.summary()
mygan.model.summary()
startvalue = 30
means = []
mygan.load_weights("lab")
for i in range(9):
    mygan.train(norm_data,batch,100,5,15)
    noise = np.random.normal(0, 1, (100, 100))
    generated_data = mygan.generator.predict(noise)
    generated_data = unnormalize(generated_data, mean, standard)
    dagplot(generated_data,iris.data,i + startvalue)
    run_folder=str(i + startvalue) + "_"
    means.append(generated_data.mean())
show_loss_progress(mygan.d_losses, mygan.g_losses, "lab")
mygan.save_model("lab2")
mp.plot(means)
mp.savefig("means.pdf")
