from core.enums import RightsRole

translate_role = {
    RightsRole.ADMIN: "Админ",
    RightsRole.STAGER: "Этапщик",
    RightsRole.SELLER: "Продавец",
    RightsRole.LOTTERY: "Лотерейщик",
}.get
