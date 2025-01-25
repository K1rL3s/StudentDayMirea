from sqlalchemy.exc import IntegrityError

from core.exceptions import (
    CouponAlreadyClaimed,
    NoFreeCoupons,
    UserNotFound,
    WrongCouponAnswer,
)
from core.ids import CouponId, UserId
from core.services.roles import RolesService
from database.repos.coupons import CouponsRepo
from database.repos.logs import LogsRepo
from database.repos.users import UsersRepo

COUPON_ANSWER = "DS25_MIREA"


class CouponsService:
    def __init__(
        self,
        coupons_repo: CouponsRepo,
        users_repo: UsersRepo,
        logs_repo: LogsRepo,
        roles_service: RolesService,
    ) -> None:
        self.coupons_repo = coupons_repo
        self.users_repo = users_repo
        self.logs_repo = logs_repo
        self.roles_service = roles_service

    async def create(self, description: str, master_id: UserId) -> CouponId:
        await self.roles_service.is_admin(master_id)
        return await self.coupons_repo.create(description)

    async def reward(self, user_id: UserId, coupon_phrase: str) -> CouponId:
        if coupon_phrase != COUPON_ANSWER:
            raise WrongCouponAnswer

        if await self.users_repo.get_by_id(user_id) is None:
            raise UserNotFound(user_id)

        if await self.coupons_repo.get_by_user_id(user_id):
            raise CouponAlreadyClaimed(user_id)

        try:
            coupon_id = await self.coupons_repo.link_user_to_random_coupon(user_id)
        except IntegrityError as e:
            raise CouponAlreadyClaimed(user_id) from e

        if coupon_id is None:
            raise NoFreeCoupons

        return coupon_id
