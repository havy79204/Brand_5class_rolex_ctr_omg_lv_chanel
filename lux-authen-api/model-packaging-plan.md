# Model Packaging Migration Plan

## Overview

Transform the codebase from a scattered 3-folder architecture (core → dependencies → features) into a modular package-based system where each model is self-contained, versioned, and manageable independently.

## Architecture Changes

### Current Structure Issues

- Model architecture in `core/models/`
- Weight loading + transforms in `dependencies/`
- Business logic in `features/`
- Shared preprocessing functions cause tight coupling
- No clear version management

### New Structure (Modular Monolith)

```
rolex-kag-api/
├── main.py                          # FastAPI app (minimal changes)
├── routers/                         # API endpoints (backward compatible)
├── model_packages/                  # NEW: Self-contained model packages
│   ├── __init__.py
│   ├── rolex_p01_v1/               # Example model package
│   │   ├── __init__.py             # Coordinator & registration
│   │   ├── config.py               # Weights path, version, thresholds
│   │   ├── architecture.py         # Model architecture (from core, optional)
│   │   ├── detector.py             # YoloBase implementation + YOLO loading
│   │   └── authenticator.py        # AuthenticateBase implementation + Auth model loading
│   ├── rolex_p02_v1/
│   ├── rolex_p03_v1/
│   ├── ... (all Rolex P01-P10)
│   ├── lv_p01_v1/
│   ├── ... (all LV models)
│   └── redframe_p01_v1/
│       └── ... (RedFrame models)
├── core/
│   └── registry.py                 # NEW: Model registration & discovery
└── legacy/                          # OLD code (archive after migration)
    ├── core/
    ├── dependencies/
    └── features/
```

## Implementation Strategy

### Phase 1: Foundation Setup

**Goal:** Create infrastructure for new system

1. **Install raiki-sdk**

   - Add to `requirements.txt` with token/SSH
   - Verify imports work

2. **Create core infrastructure**

   - `core/registry.py`: Model registry with auto-discovery

3. **Create model package template**

   - Document standard structure
   - Create example with one simple model

### Phase 2: Migrate Pilot Models (Proof of Concept)

**Goal:** Validate approach with 2-3 models

1. **Migrate Rolex P01**

   - Create `model_packages/rolex_p01_v1/`
   - Move architecture from `core/models/EfficientNetLoG.py`
   - Move logic from `dependencies/rolex/Rolex_P01.py`
   - Move business logic from `features/rolex/RolexP01.py`
   - Implement using raiki-sdk base classes
   - Register in registry

2. **Migrate LV P01**

   - Create `model_packages/lv_p01_v1/`
   - Similar migration steps

3. **Test backward compatibility**

   - Verify `/check` endpoint works identically
   - Verify `/classify` endpoint works identically
   - Compare outputs with old system

### Phase 3: Batch Migrate Remaining Models

**Goal:** Migrate all models systematically

1. **Migrate Rolex models** (P02-P10)

   - 9 model packages

2. **Migrate LV models** (P01-P05)

   - 5 model packages

3. **Migrate RedFrame models** (P01-P03)

   - 3 model packages

4. **Migrate Classification models**

   - Rolex classifier
   - LV classifier

### Phase 4: Update API Layer

**Goal:** Ensure backward compatibility

1. **Update routers/**

   - Modify `routers/check_part.py` to use registry
   - Modify `routers/classify.py` to use registry
   - Maintain exact same request/response formats
   - Keep same validation logic

2. **Update `dependencies/manager_dp.py`**

   - Replace with thin wrapper to new registry
   - Or update to delegate to `core/registry.py`

### Phase 5: Testing & Validation

**Goal:** Ensure system works identically

1. **Unit tests for each model package**

   - Test YOLO detection
   - Test authentication
   - Test preprocessing

2. **Integration tests**

   - Test all API endpoints
   - Compare with baseline outputs

3. **Load testing**

   - Verify memory usage (should be same ~24GB)
   - Verify response times

### Phase 6: Cleanup & Documentation

**Goal:** Finalize migration

1. **Archive old code**

   - Move `core/`, `dependencies/`, `features/` → `legacy/`
   - Add migration notes

2. **Update documentation**

   - Document new structure
   - Model versioning guide
   - How to add new models

3. **Update deployment**

   - Verify `uvicorn` still works same way
   - Update any deployment scripts

## Model Package Structure Detail

Each model package follows this pattern:

```python
# model_packages/rolex_p01_v1/config.py
MODEL_VERSION = "v1"
YOLO_WEIGHTS = "models/yolo_P01_v4_Dat.pt"
AUTH_WEIGHTS = "models/rolex_p01_efficientNetB4_23-05-25.pth"
THRESHOLD = 2.8
TARGET_SIZE = 224
DEVICE = "cuda"

# model_packages/rolex_p01_v1/detector.py
from raiki_sdk import YoloBase, YoloResult
from ultralytics import YOLO

class RolexP01Detector(YoloBase):
    def __init__(self):
        super().__init__(model_path=YOLO_WEIGHTS)
    
    def detect(self, image) -> YoloResult:
        # YOLO detection logic
        pass
    
    def validate(self, yolo_results, frame=None):
        # Validation logic from old validate()
        pass

# model_packages/rolex_p01_v1/authenticator.py
from raiki_sdk import AuthenticateBase, AuthResult

class RolexP01Authenticator(AuthenticateBase):
    def __init__(self, model, transform, device):
        self.model = model
        self.transform = transform
        self.device = device
    
    def authenticate(self, image) -> AuthResult:
        # Auth logic from old forward()
        pass

## Key Benefits

1. **Version Management**: Each model has clear version, easy to update one without affecting others
2. **Isolation**: Model changes don't break other models
3. **Maintainability**: All logic for one model in one folder
4. **Testability**: Each package is independently testable
5. **Backward Compatible**: Existing APIs work unchanged
6. **Deployment**: Same simple deployment (uvicorn main:app)

## Migration Risks & Mitigations

**Risk 1:** Breaking existing API behavior

- **Mitigation:** Extensive integration tests, shadow deployment

**Risk 2:** Memory usage changes

- **Mitigation:** Load all models at startup (same as now), monitor VRAM

**Risk 3:** Performance regression

- **Mitigation:** Benchmark before/after, ensure no extra overhead

**Risk 4:** Long migration time

- **Mitigation:** Pilot with 2-3 models first, then batch migrate

## Timeline Estimate

- Phase 1 (Foundation): 2-3 days
- Phase 2 (Pilot): 2-3 days
- Phase 3 (Batch Migration): 5-7 days (20+ models)
- Phase 4 (API Update): 1-2 days
- Phase 5 (Testing): 2-3 days
- Phase 6 (Cleanup): 1 day

**Total:** ~13-19 days for complete migration

## To-Do List
[x] Install raiki-sdk and add to requirements.txt  
[x] Create core infrastructure `registry.py` 
[x] Create model package template and documentation  
[x] Migrate Rolex P01 to new model package structure  
[ ] Migrate LV P01 to new model package structure  
[ ] Test backward compatibility with pilot models (P01s)  
[ ] Migrate remaining Rolex models (P02–P10)  
[ ] Migrate remaining LV models (P02–P05)  
[ ] Migrate RedFrame models (P01–P03)  
[ ] Migrate classification models (Rolex & LV classifiers)  
[ ] Update API routers to use registry while maintaining backward compatibility  
[ ] Create and run integration tests for all endpoints  
[ ] Archive old code structure to legacy folder  
[ ] Update documentation for new structure and versioning guide

### Completed ✅

_Nothing completed yet - start with Phase 1!_

