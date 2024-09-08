import os
import requests
import argparse

# 获取当前脚本所在目录的上一级目录
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def download_file(url, save_path):
    try:
        print(f"Begin downloading: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Download completed. Save to: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")


def download_models(model_urls):
    # 指定下载保存的目录
    save_dir = "hivision/creator/weights"

    # 创建目录（如果不存在的话）
    os.makedirs(os.path.join(base_path, save_dir), exist_ok=True)

    # 下载每个模型
    for model_name, model_info in model_urls.items():
        url = model_info["url"]
        file_format = model_info["format"]

        # 特殊处理 rmbg-1.4 模型的文件名
        file_name = f"{model_name}.{file_format}"

        save_path = os.path.join(base_path, save_dir, file_name)

        # 检查文件是否已经存在
        if os.path.exists(save_path):
            print(f"File already exists, skipping download: {save_path}")
            continue

        # 下载文件
        download_file(url, save_path)


def main(models_to_download):
    # 模型权重的下载链接
    model_urls = {
        "hivision_modnet": {
            "url": "https://github.com/Zeyi-Lin/HivisionIDPhotos/releases/download/pretrained-model/hivision_modnet.onnx",
            "format": "onnx",
        },
        "modnet_photographic_portrait_matting": {
            "url": "https://github.com/Zeyi-Lin/HivisionIDPhotos/releases/download/pretrained-model/modnet_photographic_portrait_matting.onnx",
            "format": "onnx",
        },
        "mnn_hivision_modnet": {
            "url": "https://github.com/Zeyi-Lin/HivisionIDPhotos/releases/download/pretrained-model/mnn_hivision_modnet.mnn",
            "format": "mnn",
        },
        "rmbg-1.4": {
            "url": "https://huggingface.co/briaai/RMBG-1.4/resolve/main/onnx/model.onnx?download=true",
            "format": "onnx",
        },
    }

    # 如果选择下载所有模型
    if "all" in models_to_download:
        selected_urls = model_urls
    else:
        selected_urls = {model: model_urls[model] for model in models_to_download}

    if not selected_urls:
        print("No valid models selected for download.")
        return

    download_models(selected_urls)


if __name__ == "__main__":
    MODEL_CHOICES = [
        "hivision_modnet",
        "modnet_photographic_portrait_matting",
        "mnn_hivision_modnet",
        "rmbg-1.4",
        "all",
    ]

    parser = argparse.ArgumentParser(description="Download matting models.")
    parser.add_argument(
        "--models",
        nargs="+",
        required=True,
        choices=MODEL_CHOICES,
        help='Specify which models to download (options: hivision_modnet, modnet_photographic_portrait_matting, mnn_hivision_modnet, rmbg-1.4, all). Only "all" will download all models.',
    )
    args = parser.parse_args()

    models_to_download = args.models if args.models else ["all"]
    main(models_to_download)
