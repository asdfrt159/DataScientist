import numpy as np


def algo(df, al_df, num, col) :
    if col == 0 : 
        if num == 1 :
            val = df[0,col] - df[2,col]
        elif num == 2 :
            val = df[0,col] - df[1,col]
        elif num == 3 :
            val = df[1,col] - df[2,col]
        elif num == 4 : 
            val = df[2,col] - df[1,col]
        elif num == 5 :
            val = df[1,col] - df[0,col]
        elif num == 6 : 
            val = df[2,col] - df[0,col]
        else : 
            val = None
        return val
    else : 
        if num == 1 :
            val = df[0,col] - df[2,col]
            val = val + max(al_df[4-1,col-1],al_df[5-1,col-1])
        elif num == 2 :
            val = df[0,col] - df[1,col]
            val = val + max(al_df[3-1,col-1],al_df[6-1,col-1])
        elif num == 3 :
            val = df[1,col] - df[2,col]
            val = val + max(al_df[2-1,col-1],al_df[6-1,col-1])
        elif num == 4 : 
            val = df[2,col] - df[1,col]
            val = val + max(al_df[1-1,col-1],al_df[5-1,col-1])
        elif num == 5 :
            val = df[1,col] - df[0,col]
            val = val + max(al_df[1-1,col-1],al_df[4-1,col-1])
        elif num == 6 : 
            val = df[2,col] - df[0,col]
            val = val + max(al_df[2-1,col-1],al_df[3-1,col-1])
        else : 
            val = None
        return val
    

def main() :
    with open('input4.txt','r') as f : 
        text = f.readlines()

    lines = [x.rstrip('\n') for x in text]
    
    arr_list = []
    for i in range(len(lines)) :
        if i%4 != 1 :
            continue
        arr_list.append(np.array([[int(x) for x in lines[i].split(' ')],[int(x) for x in lines[i+1].split(' ')],[int(x) for x in lines[i+2].split(' ')]]))

    ans = []
    # 배열 생성
    for k in range(len(arr_list)) :
        max_list = []
        arr = np.empty((6,arr_list[k].shape[1]))
        arr[:] = np.nan

        for j in range(arr_list[k].shape[1]) :  # 0 ~ 9
            for i in range(6) :  # 0 ~ 5
                arr[i, j] = algo(arr_list[k],arr,i+1, j)
        
        for i in range(6) :
            max_list.append(arr[i,arr_list[k].shape[1]-1])

        ans.append(int(max(max_list)))

    with open('output4.txt','w') as f:
        for i in range(len(ans)) :
            f.write('#'+ str(i+1) + ' ' +str(ans[i]) + '\n')

if __name__ == "__main__" :
    main()