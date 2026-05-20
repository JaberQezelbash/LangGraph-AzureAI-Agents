# datasets/

Recommended dataset categories:

1. Patient message / healthcare conversation dataset
2. Appointment or scheduling dataset
3. Hospital satisfaction or patient experience dataset
4. EHR-style patient records dataset
5. Specialty or symptom classification dataset

The cloud deployment does **not** upload full raw datasets. Instead, run:

```powershell
python codes/scripts/prepare_cloud_data.py
```

This creates a smaller cloud demo dataset under:

```text
cloud_data/processed/
```

Only this processed subset is packaged into Azure.

**The main reason was that I wanted to make this demo cheaper in terms of token usage for the later steps :)**