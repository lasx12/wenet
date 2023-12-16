import os
import pytest

from wenet.text.hugging_face_tokenizer import HuggingFaceTokenizer

try:
    import transformers  # noqa
except ImportError:
    os.system('pip install --no-input transformers')
    import transformers  # noqa


@pytest.fixture(params=["bert-base-cased"])
def hugging_face_tokenizer(request):
    return HuggingFaceTokenizer(request.param)


def test_text2tokens(hugging_face_tokenizer: HuggingFaceTokenizer):
    tokenizer = hugging_face_tokenizer
    text = "hello wenet very cool!"
    expected = ['hello', 'we', '##net', 'very', 'cool', '!']
    assert all(h == r for h, r in zip(tokenizer.text2tokens(text), expected))


def test_tokens2text(hugging_face_tokenizer: HuggingFaceTokenizer):
    tokenizer = hugging_face_tokenizer
    inputs = ['hello', 'we', '##net', 'very', 'cool', '!']
    expected = "hello wenet very cool!"

    result = tokenizer.tokens2text(inputs)
    assert result == expected


def test_tokens2ids(hugging_face_tokenizer: HuggingFaceTokenizer):
    tokenizer = hugging_face_tokenizer
    inputs = ['hello', 'we', '##net', 'very', 'cool', '!']
    expected = [19082, 1195, 6097, 1304, 4348, 106]
    tokens = tokenizer.tokens2ids(inputs)
    assert len(tokens) == len(expected)
    assert all(h == r for (h, r) in zip(tokens, expected))


def test_ids2tokens(hugging_face_tokenizer: HuggingFaceTokenizer):
    tokenizer = hugging_face_tokenizer
    ids = [19082, 1195, 6097, 1304, 4348, 106]
    expected = ['hello', 'we', '##net', 'very', 'cool', '!']
    results = tokenizer.ids2tokens(ids)
    assert len(results) == len(expected)
    assert all(h == r for (h, r) in zip(results, expected))


def test_tokenize(hugging_face_tokenizer: HuggingFaceTokenizer):
    tokenizer = hugging_face_tokenizer

    text = "hello wenet very cool!"
    ids = [19082, 1195, 6097, 1304, 4348, 106]
    tokens = ['hello', 'we', '##net', 'very', 'cool', '!']

    result = tokenizer.tokenize(text)
    for module in result["tokens"].keys():
        assert len(result["tokens"][module]) == len(tokens)
        assert all(h == r for (h, r) in zip(result["tokens"][module], tokens))
        assert len(result["label"][module]) == len(ids)
        assert all(h == r for (h, r) in zip(result["label"][module], ids))


def test_detokenize(hugging_face_tokenizer: HuggingFaceTokenizer):
    tokenizer = hugging_face_tokenizer
    text = "hello wenet very cool!"
    ids = [19082, 1195, 6097, 1304, 4348, 106]
    tokens = ['hello', 'we', '##net', 'very', 'cool', '!']

    result = tokenizer.detokenize(ids)
    for module in result["text"].keys():
        assert result["text"][module] == text
        assert len(result["tokens"][module]) == len(tokens)
        assert all(h == r for (h, r) in zip(result["tokens"][module], tokens))


def test_vocab_size(hugging_face_tokenizer: HuggingFaceTokenizer):
    assert hugging_face_tokenizer.vocab_size() == 28996
    assert hugging_face_tokenizer.vocab_size() == len(
        hugging_face_tokenizer.symbol_table)


def test_tongyi_tokenizer():
    # NOTE(Mddct): tongyi need extra matplotlib package
    os.system('pip install --no-input matplotlib')
    model_dir = 'Qwen/Qwen-Audio-Chat'
    tongyi_tokenizer = transformers.AutoTokenizer.from_pretrained(
        model_dir, trust_remote_code=True)
    tokenizer = HuggingFaceTokenizer(model_dir, trust_remote_code=True)
    text = "from transformers import AutoModelForCausalLM, AutoTokenizer"
    tongyi_result = tongyi_tokenizer.tokenize(text)
    result = tokenizer.tokenize(text)

    for module in result["tokens"].keys():
        assert len(result["tokens"][module]) == len(tongyi_result)
        assert all(h == r for (h, r) in zip(result["tokens"][module], tongyi_result))
