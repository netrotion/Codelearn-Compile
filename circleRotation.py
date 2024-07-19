# AUTHOR : TLG_KIEN
# LINK : https://codelearn.io/training/2108
def circlerotation(arr,d):
    if len(arr) > d:
        return arr[d]
    else:
        so_vong = int(d / len(arr))
        return circlerotation(arr, d - so_vong*len(arr))