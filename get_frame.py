"""
指定した動画ファイルを、指定フレームごとに画像へ変換して、指定ディレクトリに出力する
command ex.
 python video_slicer.py --name camera-mov/pin/2019-01-30_10-06-45-Schedule.mp4 --frame 150
出力例
 {指定ディレクトリ}/2019-01-30_10-06-45-Schedule/2019-01-30_10-06-45-Schedule_000000_0.jpg
"""

import argparse
import datetime
import math
import os
import cv2


def slice_video(file_path: str, interval_frame=1, save_dir='video'):
    """
    動画を画像化する
    :param file_path: str 動画ファイル名
    :param interval_frame: int 何フレームごとに切り出すか
    :param save_dir: str 切り出した画像を保存するフォルダ
    """

    # 動画ファイルを読み込む
    video = cv2.VideoCapture(file_path)

    # ファイルパスからファイル名を取り出す
    file_name = ""
    file_path_split = file_path.rsplit("/", 1)
    if len(file_path_split) == 1:
        file_name = file_path
    else:
        file_name = file_path_split[-1]

    # 拡張子の文字列を除去
    file_name = file_name.rsplit(".", 1)[0]

    # スクリーンキャプチャを保存するディレクトリ
    dir_name = os.path.join(save_dir,file_name)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    # 動画1秒あたりのフレーム数。OpenCVのバージョン3以降
    fps = video.get(cv2.CAP_PROP_FPS)
    print("1秒あたりのフレーム数:{0}".format(fps))

    # フレーム数を取得
    frame_count = int(video.get(7))
    # 出力するキャプチャのファイル名テンプレート _{動画タイム}_{余剰フレーム値}
    cap_name_template = dir_name + "/" + file_name + "_{:02}{:02}{:02}_{}.jpg"
    # 0フレームから最終フレームまでをinterval_frame値ごとにキャプチャにする
    for i in range(0, frame_count, interval_frame):
        # フレーム移動
        video.set(cv2.CAP_PROP_POS_FRAMES, i)
        # 読み出し
        is_read, frame = video.read()
        if not is_read:
            print("読み込み失敗 フレーム番号:{0}".format(i))
            continue

        # フレームから動画時間に変換
        # math.floor(i / fps)が秒数
        seconds = math.floor(i / fps)
        second = seconds % 60  # 秒
        minute = math.floor(seconds / 60)  # 分
        hour = math.floor(minute / 60)  # 時

        remainder = math.floor(i % fps)  # fpsがfloat値なので
        # 書き出し
        cv2.imwrite(cap_name_template.format(hour, minute, second, remainder), frame)

    print("finish {}".format(datetime.datetime.now()))


if __name__ == '__main__':

    # コマンドライン引数で、name必須。frameは指定可能
    parser = argparse.ArgumentParser(description='video_slice')
    parser.add_argument('--name', dest='name', type=str, help='read file name')
    parser.add_argument('--frame', dest='frame', type=int, help='interval frame count')
    parser.add_argument('--save_dir', dest='save_dir', type=str, default='screen_caps', help='image save dir')
    args = parser.parse_args()

    if args.name:
        path = args.name

        # 何フレームごとに動画スライスするか
        if args.frame:
            frames = args.frame
        else:
            frames = 1

        save_dir = args.save_dir
        # 実行
        slice_video(path, frames, save_dir)

    else:
        # nameの必須チェック
        print("Error: '--name ファイル名' の指定をしてください")
