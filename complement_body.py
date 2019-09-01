import json
import glob
import sys
from statistics import mean

def getFilelist(path):
    filelist = glob.glob(path + "/*")
    return filelist

def checkBackForward(data, i, filelist, which): # 別のフレームから腰の座標を持ってくる
    if which == "left":
        N = 24
    elif which == "right":
        N = 33
    
    for b in range(i): # とりあえず前のフレームを探す
        with open(filelist[i-b] , "r") as sub:
            subdata = json.load(sub)
            if len(subdata["people"]) != 0:
                if subdata['people'][0]['pose_keypoints_2d'][N+2] != 0:
                    data['people'][0]['pose_keypoints_2d'][N] = subdata['people'][0]['pose_keypoints_2d'][N]
                    data['people'][0]['pose_keypoints_2d'][N+1] = subdata['people'][0]['pose_keypoints_2d'][N+1]
                    return data
    
    for f in range(len(filelist)-i): # 後ろのフレームを探す
        print("right")
        with open(filelist[i+f+1] , "r") as sub:
            subdata = json.load(sub)
            if len(subdata["people"]) != 0:
                if subdata['people'][0]['pose_keypoints_2d'][N+2] != 0:
                    data['people'][0]['pose_keypoints_2d'][N] = subdata['people'][0]['pose_keypoints_2d'][N]
                    data['people'][0]['pose_keypoints_2d'][N+1] = subdata['people'][0]['pose_keypoints_2d'][N+1]
                    return data


def dynamicComplemention(data): # 動的補完(腰の動きが変化するような動画の場合はこちらを使用する．今回は使用しない)
    # もし腰の関節が認識されていなかった場合，別のフレームのものを読み込む
    if data['people'][0]['pose_keypoints_2d'][26] == 0:
        print("左腰関節行方不明")
        data = checkBackForward(data, i, filelist, "left")                 

    elif data['people'][0]['pose_keypoints_2d'][35] == 0:        
        print("右腰関節行方不明")
        data = checkBackForward(data, i, filelist, "right")   

def staticComplemention(filelist): # 静的な補完を行う(全部のフレームを解析し，その平均を全体に適応する)
    leftwaistx = []
    leftwaisty = []
    rightwaistx = []
    rightwaisty = []
    leglen = []
    for i in range(len(filelist)):
        with open(filelist[i] , "r") as f:
            
            sdata = json.load(f)
            if len(sdata["people"]) != 0:
                if sdata['people'][0]['pose_keypoints_2d'][26] != 0:
                    leftwaistx.append(sdata['people'][0]['pose_keypoints_2d'][24])
                    leftwaisty.append(sdata['people'][0]['pose_keypoints_2d'][25])
                    leglen.append((sdata['people'][0]['pose_keypoints_2d'][25] - sdata['people'][0]['pose_keypoints_2d'][1])/2)
                if sdata['people'][0]['pose_keypoints_2d'][35] != 0:
                    rightwaistx.append(sdata['people'][0]['pose_keypoints_2d'][33])
                    rightwaisty.append(sdata['people'][0]['pose_keypoints_2d'][34])

    return mean(leftwaistx),mean(leftwaisty), mean(rightwaistx), mean(rightwaisty), mean(leglen)


def legsComplemention(filelist): # 腰より下の部分を補完する
    # 補完データの取得
    waist = staticComplemention(filelist)
    for i in range(len(filelist)):
        
        with open(filelist[i] , "r") as f:
            print(filelist[i])
            data = json.load(f)

            # ヒト認識がうまくいっていない場合は以下の処理を行わない．
            if len(data["people"]) != 0:

                # 腰の補完を行う(静的)
                data['people'][0]['pose_keypoints_2d'][24] = waist[0]
                data['people'][0]['pose_keypoints_2d'][25] = waist[1]
                data['people'][0]['pose_keypoints_2d'][33] = waist[2]
                data['people'][0]['pose_keypoints_2d'][34] = waist[3]

                # leg length(足の1関節の長さを0と8のyの差で定める)
                leglen = waist[4]

                # position 9
                data['people'][0]['pose_keypoints_2d'][27] = data['people'][0]['pose_keypoints_2d'][24]
                data['people'][0]['pose_keypoints_2d'][28] = data['people'][0]['pose_keypoints_2d'][25] + leglen

                # position 10
                data['people'][0]['pose_keypoints_2d'][30] = data['people'][0]['pose_keypoints_2d'][24]
                data['people'][0]['pose_keypoints_2d'][31] = data['people'][0]['pose_keypoints_2d'][28] + leglen

                # position 12
                data['people'][0]['pose_keypoints_2d'][36] = data['people'][0]['pose_keypoints_2d'][33]
                data['people'][0]['pose_keypoints_2d'][37] = data['people'][0]['pose_keypoints_2d'][34] + leglen

                # position 13
                data['people'][0]['pose_keypoints_2d'][39] = data['people'][0]['pose_keypoints_2d'][33]
                data['people'][0]['pose_keypoints_2d'][40] = data['people'][0]['pose_keypoints_2d'][37] + leglen

                with open(filelist[i], "w") as f:
                    # write json
                    json.dump(data, f)



def main():
    print(sys.argv[1])
    try:    
        filelist = getFilelist(sys.argv[1])
        legsComplemention(filelist)
    except:
        import traceback
        traceback.print_exc()
main()
