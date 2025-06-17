# AI Agricultural Assistance

Built a machine learning-powered web application that brings together multiple tools to assist farmers and agronomists with data-driven agricultural decisions.

🎯 The system includes five major features:

✅ Crop disease classification using image processing models such as DenseNet201, VGG19, Xception, InceptionResNetV2, and MobileNetV2 through Transfer Learning. The best model achieved 99% accuracy on the validation set.

✅ Crop yield prediction, crop recommendation, and fertilizer recommendation powered by supervised machine learning models like CatBoost, Random Forest, and XGBoost, achieving around 96% accuracy across tasks.

✅ Geolocation-based crop identification, allowing users to place a pointer on a Google Map of India and detect the likely crop grown in that region.

For every feature, I compared multiple models and performed Bayesian hyperparameter tuning using Optuna and Hyperopt to select the best model for each task.

The datasets used for model training and testing were sourced from Kaggle and Indian agricultural datasets, ensuring regional relevance and model robustness.

The solution is deployed via a custom-built frontend using HTML, CSS, and JavaScript, offering an accessible and intuitive interface for end-users.

🔧 Tech Stack: HTML, CSS, JavaScript, Google Maps API, Scikit-learn, TensorFlow, XGBoost, CatBoost, Random Forest, DenseNet201, VGG19, Xception, InceptionResNetV2, MobileNetV2, Optuna, Hyperopt.
