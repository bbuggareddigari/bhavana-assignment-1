
rm -v /tmp/detectron-visualizations/*.pdf ; rm -v ~/run/*.jpg ; rm -v ./output.txt ; python3 viewer.py ; python ~/Detectron/tools/infer_simple.py --cfg ~/Detectron/configs/12_2017_baselines/e2e_mask_rcnn_R-101-FPN_2x.yaml --output-dir /tmp/detectron-visualizations --image-ext jpg --wts https://dl.fbaipublicfiles.com/detectron/35861858/12_2017_baselines/e2e_mask_rcnn_R-101-FPN_2x.yaml.02_32_51.SgT4y1cO/output/train/coco_2014_train:coco_2014_valminusminival/generalized_rcnn/model_final.pkl /home/controller/run && python convert-pdf-text-and-speak-it.py output.txt /tmp/detectron-visualizations/frame0.jpg.pdf && qpdfview /tmp/detectron-visualizations/frame0.jpg.pdf
