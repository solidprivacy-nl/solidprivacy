from __future__ import annotations

from typing import Any


PINNED_PRESCAN_COMMIT = "d8d690989da03287b8879ba1319f78ca8a404bd5"
PINNED_PRESCAN_VERSION = "2.0"

EDPB_OPTIONS = {
    "Lijst EDPB: Bijzondere persoonsgegevens of zeer gevoelige persoonsgegevens": "sensitive_data",
    "Lijst EDPB: Blokkering van een dienst, recht of contract": "rights_or_service_blocking",
    "Lijst EDPB: Geautomatiseerde besluitvorming": "automated_decision_significant_effect",
    "Lijst EDPB: Gebruik van nieuwe technologieën": "innovative_technology",
    "Lijst EDPB: Grootschalige gegevensverwerkingen": "large_scale",
    "Lijst EDPB: Koppelen van datasets": "matching_datasets",
    "Lijst EDPB: Mensen beoordelen met persoonskenmerken (evaluatie of scoring)": "evaluation_or_scoring",
    "Lijst EDPB: Stelselmatige en grootschalige monitoring": "systematic_monitoring",
    "Lijst EDPB: Verwerking van persoonsgegevens over kwetsbare groepen of personen": "vulnerable_data_subjects",
}

AP_OPTIONS = {
    "Lijst AP: Biometrische gegevens": "biometric_data",
    "Lijst AP: Cameratoezicht": "camera_surveillance",
    "Lijst AP: Communicatiegegevens": "communications_data",
    "Lijst AP: Controle werknemers": "employee_monitoring",
    "Lijst AP: Creditscores": "credit_scoring",
    "Lijst AP: Financiële situatie": "financial_situation",
    "Lijst AP: Flexibel cameratoezicht": "flexible_camera_surveillance",
    "Lijst AP: Fraudebestrijding": "fraud_prevention",
    "Lijst AP: Genetische persoonsgegevens": "genetic_data",
    "Lijst AP: Gezondheidsgegevens": "health_data",
    "Lijst AP: Heimelijk onderzoek": "covert_investigation",
    "Lijst AP: Internet of things": "internet_of_things",
    "Lijst AP: Profilering": "profiling",
    "Lijst AP: Observatie en beïnvloeding van gedrag": "behaviour_observation_influence",
    "Lijst AP: Locatiegegevens": "location_data",
    "Lijst AP: Samenwerkingsverbanden": "data_sharing_partnerships",
    "Lijst AP: Zwarte lijsten": "blacklists",
}

VULNERABLE_OPTIONS = {
    "Categorie betrokkenen: Kinderen jonger dan 16 jaar": 3,
    "Categorie betrokkenen: Andere kwetsbare groepen (gehandicapten, minderheden, etc.)": 3,
}
SUBJECT_WEIGHTS = {
    "Categorie betrokkenen: Medewerkers/bewindspersonen": 1,
    "Categorie betrokkenen: Burgers over wie gegevens worden verwerkt in het proces/systeem/applicatie": 1,
    **VULNERABLE_OPTIONS,
    "Categorie betrokkenen: Specificatie categorie betrokkenen (bijv. vanuit uitvoeringswetgeving)": 0,
}

BASISREGISTRATION_WEIGHTS = {
    "Basisregistratie Grootschalige Topografie (BGT)": 0,
    "Basisregistratie Inkomen (BRI)": 1,
    "Basisregistratie Kadaster (BRK)": 1,
    "Basisregistratie Ondergrond (BRO)": 0,
    "Basisregistratie Personen (BRP)": 1,
    "Basisregistratie Topografie (BRT)": 0,
    "Basisregistratie Voertuigen (BRV)": 1,
    "Basisregistratie Waarde Onroerende Zaken (WOZ)": 1,
    "Handelsregister (HR)": 1,
    "Adressen en Gebouwen (BAG)": 0,
}


def _list(answers: dict[str, Any], key: str) -> list[Any]:
    value = answers.get(key)
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _truthy(answers: dict[str, Any], key: str) -> bool:
    return answers.get(key) is True


def _score_count(count: int, medium_upper: int = 6) -> int:
    if count <= 0:
        return 0
    if count <= medium_upper:
        return 1
    return 2


def _international_transfer_score(answers: dict[str, Any]) -> int:
    transfer = _truthy(answers, "2.1.1")
    special = _truthy(answers, "2.1.8")
    outside = answers.get("2.1.3") == "Buiten EER" or answers.get("2.1.4") == "Buiten EER"
    if transfer and (special or outside):
        return 2
    if transfer or outside:
        return 1
    return 0


def methodology_risk_score(answers: dict[str, Any]) -> tuple[int, dict[str, int]]:
    ordinary_count = len(_list(answers, "1.1.2")) if _truthy(answers, "1.1.1") else 0
    ordinary = 1 if ordinary_count >= 6 else 0

    special_count = len(_list(answers, "1.2.2")) if _truthy(answers, "1.2.1") else 0
    special = _score_count(special_count)

    sensitive_count = len(_list(answers, "1.3.2")) if _truthy(answers, "1.3.1") else 0
    sensitive = _score_count(sensitive_count)

    subject_weight = sum(SUBJECT_WEIGHTS.get(item, 0) for item in _list(answers, "1.4.1"))
    if subject_weight <= 2:
        subjects = 0
    elif subject_weight == 3:
        subjects = 1
    else:
        subjects = 2

    data_subject_count = 1 if _truthy(answers, "1.5.1") else 0

    frequency = 1 if answers.get("1.5.3") in {
        "Minstens maandelijks",
        "Vaker dan maandelijks",
        "Continu",
    } else 0

    retention = 1 if answers.get("1.5.4") in {"Jaar", "Aantal jaren"} else 0

    international = _international_transfer_score(answers) if _truthy(answers, "2.1.1") else 0

    basis_weight = sum(
        BASISREGISTRATION_WEIGHTS.get(item.replace("Basisregistratie: ", ""), 0)
        for item in _list(answers, "5.1.2")
    ) if _truthy(answers, "5.1.1") else 0
    basisregistration = 1 if basis_weight >= 1 else 0

    if _truthy(answers, "7.1.2"):
        children_service = 2
    elif _truthy(answers, "7.1.1") and answers.get("7.1.3") is not True:
        children_service = 1
    else:
        children_service = 0

    components = {
        "ordinary_personal_data": ordinary,
        "special_personal_data": special,
        "sensitive_personal_data": sensitive,
        "vulnerable_or_multiple_subject_context": subjects,
        "data_subject_count": data_subject_count,
        "processing_frequency": frequency,
        "retention": retention,
        "international_transfer": international,
        "basisregistration": basisregistration,
        "digital_service_minors": children_service,
    }
    return sum(components.values()), components


def methodology_decision(answers: dict[str, Any]) -> dict[str, Any]:
    risk_score, components = methodology_risk_score(answers)
    ap_items = _list(answers, "3.1")
    edpb_items = _list(answers, "4.1")

    required_reasons: list[str] = []
    if _truthy(answers, "0.1"):
        required_reasons.append("new_legislation_scope")
    if risk_score > 4:
        required_reasons.append("rijksmodel_risk_score_gt_4")
    if len(ap_items) >= 1:
        required_reasons.append("ap_list_item_selected")
    if len(edpb_items) >= 2:
        required_reasons.append("edpb_two_or_more_criteria")

    if required_reasons:
        level = "required"
    elif len(edpb_items) == 1:
        level = "recommended"
    else:
        level = "not_indicated"

    return {
        "level": level,
        "risk_score": risk_score,
        "risk_components": components,
        "ap_list_count": len(ap_items),
        "ap_list_items": [AP_OPTIONS.get(item, item) for item in ap_items],
        "edpb_criteria_count": len(edpb_items),
        "edpb_criteria": [EDPB_OPTIONS.get(item, item) for item in edpb_items],
        "reasons": required_reasons or (["edpb_one_criterion"] if len(edpb_items) == 1 else []),
        "source": {
            "source_id": "nl-government-par-dpia-model",
            "version": f"{PINNED_PRESCAN_VERSION}@{PINNED_PRESCAN_COMMIT}",
            "locator": "sources/prescan.yaml#assessments.DPIA",
            "classification": "OFFICIAL_METHODOLOGY",
        },
    }


def _direct_article_35_3_triggers(legal_context: dict[str, Any]) -> list[str]:
    article = legal_context.get("article_35_3") or {}
    return [
        name
        for name in (
            "systematic_extensive_automated_evaluation_significant_effect",
            "large_scale_special_or_criminal_data",
            "large_scale_systematic_public_monitoring",
        )
        if article.get(name) is True
    ]


def _legal_context_complete(legal_context: dict[str, Any]) -> bool:
    article = legal_context.get("article_35_3") or {}
    direct_values = [
        article.get("systematic_extensive_automated_evaluation_significant_effect"),
        article.get("large_scale_special_or_criminal_data"),
        article.get("large_scale_systematic_public_monitoring"),
        legal_context.get("law_or_regulation_requires_dpia"),
        legal_context.get("ap_list_selection_verified"),
    ]
    return all(value is not None for value in direct_values)


def legal_decision(
    answers: dict[str, Any],
    legal_context: dict[str, Any],
    methodology: dict[str, Any],
) -> dict[str, Any]:
    direct_triggers = _direct_article_35_3_triggers(legal_context)
    ap_count = methodology["ap_list_count"]
    edpb_count = methodology["edpb_criteria_count"]
    reasons: list[dict[str, Any]] = []

    if direct_triggers:
        for trigger in direct_triggers:
            reasons.append({
                "id": f"gdpr_art_35_3:{trigger}",
                "classification": "LAW_REQUIRED",
                "source_id": "eu-gdpr-eurlex",
            })
        decision = "DPIA_REQUIRED"
    elif legal_context.get("law_or_regulation_requires_dpia") is True:
        reasons.append({
            "id": "applicable_law_requires_dpia",
            "classification": "LAW_REQUIRED",
            "source_id": "eu-gdpr-eurlex",
        })
        decision = "DPIA_REQUIRED"
    elif ap_count and legal_context.get("ap_list_selection_verified") is True:
        reasons.append({
            "id": "verified_nl_ap_mandatory_list_match",
            "classification": "LAW_REQUIRED",
            "source_id": "nl-ap-dpia-mandatory-list-2019",
        })
        decision = "DPIA_REQUIRED"
    elif ap_count and legal_context.get("ap_list_selection_verified") is not True:
        reasons.append({
            "id": "unverified_nl_ap_list_selection",
            "classification": "ASSUMPTION",
            "source_id": "nl-ap-dpia-mandatory-list-2019",
        })
        decision = "NEEDS_REVIEW"
    elif edpb_count >= 2:
        reasons.append({
            "id": "edpb_two_or_more_criteria",
            "classification": "REGULATOR_GUIDANCE",
            "source_id": "edpb-dpia-guidelines-wp248",
        })
        decision = "DPIA_RECOMMENDED"
    elif edpb_count == 1:
        reasons.append({
            "id": "edpb_single_criterion_can_still_require_dpia",
            "classification": "REGULATOR_GUIDANCE",
            "source_id": "edpb-dpia-guidelines-wp248",
        })
        decision = "DPIA_RECOMMENDED"
    elif methodology["risk_score"] > 4 or "new_legislation_scope" in methodology["reasons"]:
        reasons.append({
            "id": "rijksmodel_methodology_requires_contextual_legal_review",
            "classification": "ASSUMPTION",
            "source_id": "nl-government-par-dpia-model",
        })
        decision = "NEEDS_REVIEW"
    elif not _legal_context_complete(legal_context):
        reasons.append({
            "id": "legal_context_incomplete",
            "classification": "ASSUMPTION",
            "source_id": "eu-gdpr-eurlex",
        })
        decision = "NEEDS_REVIEW"
    else:
        decision = "DPIA_NOT_INDICATED"
        reasons.append({
            "id": "no_recorded_high_risk_indicator",
            "classification": "ASSUMPTION",
            "source_id": "eu-gdpr-eurlex",
        })

    return {
        "decision": decision,
        "reasons": reasons,
        "requires_human_review": decision != "DPIA_NOT_INDICATED",
    }


def evaluate_prescan(payload: dict[str, Any]) -> dict[str, Any]:
    answers = payload["answers"]
    legal_context = payload.get("legal_context") or {}
    methodology = methodology_decision(answers)
    legal = legal_decision(answers, legal_context, methodology)

    return {
        "decision_version": "1.0",
        "input": {
            "source_model": payload["source_model"],
            "source_version": payload["source_version"],
            "source_commit": payload.get("source_commit"),
        },
        "methodology": methodology,
        "legal": legal,
        "human_review": {
            "required": legal["requires_human_review"],
            "status": "pending" if legal["requires_human_review"] else "not_required",
            "reasons": [item["id"] for item in legal["reasons"]],
        },
        "source_versions": [
            f"nl_rijksmodel_prescan:{PINNED_PRESCAN_VERSION}@{PINNED_PRESCAN_COMMIT}",
            "gdpr:2016/679",
            "edpb:wp248rev01",
            "nl_ap_dpia_list:stcrt-2019-64418",
        ],
    }
