# OpenPose 下半身補完プログラム
[FCRN-DepthPrediction-vmd](https://github.com/miu200521358/FCRN-DepthPrediction-vmd.git)の前にOpenPoseの出力データの下半身を修正するプログラムです．<br>
上半身のみに動きがあり，下半身は動かないといった動画にのみ応用が可能です．
## 動作環境
[MMDモーショントレース自動化への挑戦](https://qiita.com/miu200521358/items/d826e9d70853728abc51)のうち，[ローカル版バルクバッチ](https://github.com/miu200521358/motion_trace_bulk)での使用を前提としています．<br>
また，通常の3d-pose-baseline-vmdの代わりにこちらの[3d-pose-baseline-vmd](https://github.com/errno-mmd/3d-pose-baseline-vmd/tree/add_leg)での動作を確認しています．<br>

## 使用方法
complement_body.py を FCRN-DepthPrediction-vmd のフォルダに入れてください．<br>
また，[motion_trace_bulk-master](https://github.com/miu200521358/motion_trace_bulk) のうち，BulkDepth.bat を このBulkDepth.batに置き換えてください．

## 従来までの問題点と解決手法
腰が映る程度の上半身動画データのみを扱う際に，OpenPoseによって勝手に下半身の座標が固定されてしまうため，その後の処理に悪影響が及んでしまいます．<br>
このプログラム(complement_body.py)ではすべての動画フレームをまず解析し，腰の位置の平均を求め，すべてのフレームの腰座標，膝，足首の座標を固定します．<br>

## 腰の位置が変化する場合
現在公開分では腰の位置が変化しないような場合を想定していますが，dynamicComplemention関数を使うことで動的に補完することもできます．<br>
その場合はソースコードを書き換えてご使用ください．そのうちそれを含めて修正します．

# Licence
MIT