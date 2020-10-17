1.修改文件week19/week19code-CVPR19-Face-Anti-spoofing/process/data_helper.py中关于数据地址的变量：DATA_ROOT,TRN_IMGS_DIR,TST_IMGS_DIR等。week19/week19code-CVPR19-Face-Anti-spoofing/process/data_helper.py ![1602956325(1)](F:\cv\work\live_face_recognation_work\lesson-03\1602956325(1).png)





2. 修改完成后，运行命令：python data_fusion.py 可检查数据设置是否正确!

   ![1602956288(1)](F:\cv\work\live_face_recognation_work\lesson-03\1602956288(1).png)

3. 数据设置正确后，运行训练命令：CUDA_VISIBLE_DEVICES=0 python train_CyclicLR.py --model=model_A --image_mode=color --image_size=48![1602957574(1)](F:\cv\work\live_face_recognation_work\lesson-03\1602957574(1).png)

![1602957727(1)](F:\cv\work\live_face_recognation_work\lesson-03\1602957727(1).png)