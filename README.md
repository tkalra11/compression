## **Running the script**
To run the scripts, CompressAI package is needed.

In working folder, preferably using a virtual environment,

`git  clone  https://github.com/InterDigitalInc/CompressAI  compressai`

`cd  compressai`

` pip  install  .`

Add all images as `.npy` files in the `samples/inputs/` folder. Then simply run the `compress.py` file. The scripts use two models from the compressai package, **bmshj2018_factorized** and **bmshj2018_factorized_relu** for compression.
This can be altered in the compress.py file by altering the loop in main block.

## **Results**
The results for the compression can be found in the `samples/output.txt` file. For this particular iteration, the following results were obtained.

>### Model : bmshj2018_factorized
>
>Time : 763.7745847000042
>
>PSNR Range : (71.8751, 106.4426)
>
>MS-SSIM Range : (1.0, 1.0)
>
>Minimum compression in size(for a patch) : 1709
>
>Maximum compression in size(for a patch) : 1679442


>### Model : bmshj2018_factorized_relu
>
>Time : 855.0026123999851
>
>PSNR Range : (71.8751, 106.4426)
>
>MS-SSIM Range : (1.0, 1.0)
>
>Minimum compression in size(for a patch) : 1709
>
>Maximum compression in size(for a patch) : 1679442
