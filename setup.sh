models=(
    "dolly-v2-3b"
    "dolly-v2-7b"
    "dolly-v2-12b"
)
folders=(
    "dolly_v2_3b"
    "dolly_v2_7b"
    "dolly_v2_12b"
)
PS3="Select the Dolly 2.0 model to install: "
if [ ! -d ${folders[0]} ] && [ ! -d ${folders[1]} ] && [ ! -d ${folders[2]} ]; then
    select option in "Install ${models[0]} [~5.6 GB]?" "Install ${models[1]} [~13.8 GB]?" "Install ${models[2]} [~23.8 GB]?"
    do
        index=$(($REPLY - 1))
        model=${models[$index]}
        folder=${folders[$index]}
        git lfs install
        git clone --depth 1 https://huggingface.co/databricks/$model $folder
        sed -i "s/MODELFOLDER/$folder/g" dolly.py
    done
fi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt