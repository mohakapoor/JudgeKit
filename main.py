from src.agent import get_test_reponse
def main():
    question = """
    Query: "Where is synthetic Captcha Dataset class written?"

    LLM Answer: "The synthetic CAPTCHA dataset class is defined in the file **`src/captcha_dataset.py`**. \n\nThis is referenced in `train_sanity.py` (lines 1-9), where it is imported as:\n`from src.captcha_dataset import CaptchaDataset`"

    Context: 
            "def generate_test_captcha(text, filename, width=256, height=60):\n    \"\"\"Generate a test CAPTCHA image using enhanced generation.\"\"\"\n    # Use the enhanced CAPTCHA generation from generateCaptcha.py\n    img = generate_captcha(text, width=width, height=height)\n    \n    # Ensure results directory exists\n    os.makedirs(cfg.RESULT_DIR, exist_ok=True)\n    \n    filepath = os.path.join(cfg.RESULT_DIR, filename)\n    img.save(filepath)\n    print(f\"Generated enhanced test CAPTCHA: {filename}\")\n    return filepath",
            "import os\nimport torch\nimport torch.nn as nn\nfrom torch.utils.data import DataLoader\nfrom src.config import cfg\nfrom src.collate import ctc_collate\nfrom src.captcha_dataset import CaptchaDataset\nfrom src.vocab import vocab_size, ctc_greedy_decode\nfrom src.model_crnn import CRNN",
            "from captcha.image import ImageCaptcha\nimport random, string, os, csv, io\nimport pandas as pd\nfrom PIL import Image, ImageDraw, ImageFilter\nimport numpy as np\nimport cv2\nDATASET_DIR = \"Dataset/captchas\"\nLABELS = \"Dataset/labels.csv\"\nNUM_IMAGES = 100000\nCHARS = string.ascii_letters + string.digits\nCAPTCHA_LEN_LOWER_LIMIT = 5\nCAPTCHA_LEN_UPPER_LIMIT = 7\ndirectories = [[\"train\",0.8],[\"val\",0.1],[\"test\",0.1]]\nIMG_WIDTH = 256   # W_max from config\nIMG_HEIGHT = 60   # H from config\nGRAYSCALE = True  # grayscale from config",
            "This project implements an end-to-end CAPTCHA OCR system that can recognize text in CAPTCHA images. It uses:\n- **Synthetic CAPTCHA generation** for training data\n- **CRNN (CNN + RNN) architecture** for sequence recognition\n- **CTC (Connectionist Temporal Classification)** loss for training\n- **PyTorch** with CUDA support for GPU acceleration",
            "A PyTorch-based CAPTCHA recognition system using synthetic data generation and CTC-based sequence modeling. Built with deep learning techniques, achieving high accuracy on complex text recognition tasks."

    Ground Truth:
    "The synthetic CaptchaDataset class is located in src/captcha_dataset.py."
    """

    return get_test_reponse(question)


if __name__ == "__main__":
    print(main())
