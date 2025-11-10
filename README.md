# ReadME

## Project summary
This project investigates image-based emotion classification using a small CNN. The goal is to compare preprocessing strategies (simple resizing vs resizing + padding) and image channels (colour vs greyscale) to see which yields better classification performance on the curated dataset.

## Hypotheses
- Classification will be more successful with padding + resizing on images because resizing alone causes distortion.
- There will be a positive correlation between contrast and classification accuracy.
- The 5 negative emotions will more often be misclassified to each other than to the positive emotion (happy).

## Data
- Raw images were preprocessed and exported to CSVs used by the notebooks:
  - `./Data/Processed/df_resized.csv`
  - `./Data/Processed/df_resized_padded.csv`
- Each CSV contains image file paths, greyscale image paths, numeric features (luminance, contrast), subfolder (label), and encoded labels.


## Notebooks and App
- `jupyter_notebooks/CNN.ipynb` — model building, training, evaluation, confusion matrices for:
  - Resized colour images
  - Resized + padded colour images
  - Resized greyscale images
- `jupyter_notebooks/Visualisations.ipynb` — statistical tests and plots (boxplots, correlations, misclassification analysis).
- `app_pages/Results.py` — Streamlit dashboard showing confusion matrices, sunburst misclassification flows and summary metrics.

## Methods
- Labels encoded with `LabelEncoder`; train/val/test splits created with stratification.
- Images loaded via `tf.data` pipelines with on-the-fly augmentation (flip, rotation, zoom).
- CNN: simple Sequential model (Conv2D → Pool → Conv2D → Pool → Flatten → Dense → Softmax).
- Loss: `sparse_categorical_crossentropy`, optimizer: `adam`.
- Evaluation: accuracy, confusion matrices and per-class misclassification analysis.

## Key results
- Classification accuracy ranged ~37–41% (better than chance but low overall).
- Resized vs resized+padded: no clear advantage observed on this dataset (e.g., 37% vs 39%).
- No strong, statistically significant correlation between contrast or luminance and correct classification in the tests performed.
- Misclassification patterns are visualised with confusion matrices and sunburst charts to inspect where true labels are predicted incorrectly.
- There was no tendency for misclassified negative emotions to be to other negative emotions
- Note: The above key insights were selected with help from AI copilot for "storytelling"

## How to run
1. Create a Python environment and install dependencies:
   - recommended: Python 3.8+
   - pip install -r requirements.txt
   - Typical packages: tensorflow, numpy, pandas, matplotlib, seaborn, plotly, streamlit, scikit-learn, scipy, opencv-python
2. Jupyter notebooks:
   - Start Jupyter and run `jupyter_notebooks/CNN.ipynb` top-to-bottom (restart the kernel between heavy TF runs if needed).
3. Streamlit dashboard:
   - Ensure `st.session_state.df` is populated (or modify `Results.py` to load `./Data/Processed/results.csv`).
   - Run: `streamlit run app_pages/Results.py`
4. Reproduce plots:
   - `jupyter_notebooks/Visualisations.ipynb` reads `./Data/Processed/results.csv`.

## File structure (key files)
- `jupyter_notebooks/CNN.ipynb` — training and evaluation
- `jupyter_notebooks/Visualisations.ipynb` — analysis + plots
- `app_pages/Results.py` — Streamlit dashboard
- `Data/Processed/` — processed CSVs and dashboard images
- `README.md` — this file

## Notes & limitations
- Dataset size is relatively small; results are limited by data quantity and class imbalance.
- Simple CNN architecture was used for clarity; improved performance likely with transfer learning (pretrained backbones) and hyperparameter tuning.
- `tf.data` pipelines consume iterators — avoid iterating `test_ds` after calling `.predict()` to prevent "End of sequence" errors.
- Some notebook cells assume label encoding order; verify `LabelEncoder().classes_` before mapping integers → names.

## Next steps
- Train with larger dataset and use transfer learning (e.g., MobileNetV2, EfficientNet) with fine-tuning.
- Add cross-validation and more robust hyperparameter search.
- Improve dataset balancing or use class-weighting / focal loss.
- Persist model checkpoints and add inference script for single-image prediction.
- Expand Streamlit dashboard with interactive per-class precision/recall and sample image viewer.

## Reproducibility
- Use fixed random seeds in data splitting and model training where appropriate.
- Save the final model and encoder mapping (`encoder.classes_`) to reproduce label-name mappings.

## Dataset attribution
This project uses images from a public dataset

- Dataset name: [6 Human Emotions for image classification]
- Source / URL: [https://www.kaggle.com/datasets/yousefmohamed20/sentiment-images-classifier]
- Authors / Maintainers: [Yousef Mohamed]
- License / Terms: [e.g. CC BY 4.0, MIT, Kaggle terms]


## Ethics & Responsible AI
This project performs automatic emotion classification from facial images. Emotion recognition raises several ethical concerns; the following points summarise these and recommend mitigations. They are intentionally general so you can adapt them to your dataset and deployment context.

- Data privacy & consent: N/A dataset using public stock images.
- Bias and fairness: Facial datasets frequently under-represent specific demographic groups (age ranges, skin tones, genders, cultural expressions). Evaluate model performance across subgroups and report per-group metrics (precision/recall). If significant disparities appear, do not deploy the model for decisions that affect people until data and model fairness are addressed.
- Transparency: Document dataset provenance, preprocessing steps, label sources, and known limitations. Include an accessible summary in the dashboard and a more detailed reflective note in the notebooks.
- Human oversight and scope: Emotion classification is noisy and context-dependent. Avoid automated, high-stakes decisions based on model output (employment, security, mental-health diagnosis). Treat model predictions as exploratory signals that require human review.
- Data minimisation & retention: Keep only the data necessary for the stated research goals. Define a retention policy and securely delete images and derived artifacts when no longer needed.

## Legal & Data Governance (high level)
Describe legal responsibilities and governance steps you took (or should take) when working with personal image data. consult legal counsel for production deployments. Dataset is public stock images generally N/A but general considerations would include:

- Applicable law: If people in the dataset are EU residents, GDPR applies. Other jurisdictions may have additional privacy laws. 
- Lawful basis and consent: Record the lawful basis for processing (e.g. explicit consent for research). Maintain proof of consent and dataset licence.
- Data subject rights: Be prepared to comply with requests to remove or access personal data. In practice, keep an index of images and their sources to support takedown/requests.
- Security and access control: Store raw images and processed data in access-controlled storage. Avoid storing plaintext sensitive metadata and use encrypted backups.
- Data minimisation: Share only aggregated, non-identifying results in public artefacts. If you publish CSVs, prefer derived features (e.g. luminance/contrast) or ensure images are removed/anonymised.

## Social implications and chatbot/automation caution
Emotion recognition models are often proposed for conversational agents or analytics (e.g., chatbots that "sense" user mood). The following cautions should be considered:

- Probabilistic outputs: Emotion predictions are uncertain and context-dependent. Chatbots using emotion signals should treat them as probabilistic cues and avoid definitive statements about a user's state.
- Psychological harm and misinterpretation: Incorrect emotion inferences can cause embarrassment, distress, or wrongful action. Provide clear user opt-in/opt-out and avoid automated escalation based solely on model output.
- Misuse and surveillance risk: Emotion-detection can be misused for surveillance, targeted manipulation, or discriminatory profiling. Document acceptable uses and explicitly prohibit harmful applications in your project notes.

## Limitations and recommended next steps
- Small dataset and limited demographic coverage likely limit generalisability. Consider collecting more balanced data or using transfer learning with large, responsibly-curated datasets.
- Add per-group evaluation (confusion matrices and metrics by subgroup) to detect bias earlier.
- For deployments: apply model cards or data sheets to surface limitations, intended use-cases, and ethical constraints.