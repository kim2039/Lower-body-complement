import json
import glob
import sys

def getFilelist(path):
    filelist = glob.glob(path + "/*")
    return filelist

def checkBackForward(data, i, filelist, which):
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


def writeJson(filelist):
    for i in range(len(filelist)):
        
        with open(filelist[i] , "r") as f:
            print(filelist[i])
            data = json.load(f)

            # ヒト認識がうまくいっていない場合は以下の処理を行わない．
            if len(data["people"]) != 0:

                # もし腰の関節が認識されていなかった場合，別のフレームのものを読み込む
                if data['people'][0]['pose_keypoints_2d'][26] == 0:
                    print("左腰関節行方不明")
                    data = checkBackForward(data, i, filelist, "left")                 

                elif data['people'][0]['pose_keypoints_2d'][35] == 0:        
                    print("右腰関節行方不明")
                    data = checkBackForward(data, i, filelist, "right")                

                # leg length(足の1関節の長さを0と8のyの差で定める)
                leglen = (data['people'][0]['pose_keypoints_2d'][25] - data['people'][0]['pose_keypoints_2d'][1])/2

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
        writeJson(filelist)
    except:
        import traceback
        traceback.print_exc()
main()
