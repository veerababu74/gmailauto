from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.crud.base import CRUDBase
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate


class CRUDAgent(CRUDBase[Agent, AgentCreate, AgentUpdate]):
    def create(self, db: Session, *, obj_in: AgentCreate) -> Agent:
        """Create a new agent with unique agent_name validation"""
        try:
            return super().create(db=db, obj_in=obj_in)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Agent name already exists. Please choose a different name.",
            )

    def get_by_agent_name(self, db: Session, *, agent_name: str) -> Optional[Agent]:
        """Get agent by agent_name"""
        return db.query(Agent).filter(Agent.agent_name == agent_name).first()

    def get_active_agents(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Agent]:
        """Get all active agents"""
        return (
            db.query(Agent)
            .filter(Agent.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_agents(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Agent]:
        """Get all agents (active and inactive)"""
        return db.query(Agent).offset(skip).limit(limit).all()

    def update_agent_status(
        self, db: Session, *, agent_id: int, is_active: bool
    ) -> Optional[Agent]:
        """Update agent active status"""
        agent = self.get(db=db, id=agent_id)
        if agent:
            agent.is_active = is_active
            db.add(agent)
            db.commit()
            db.refresh(agent)
        return agent

    def delete_agent(self, db: Session, *, agent_id: int) -> Optional[Agent]:
        """Soft delete an agent by setting is_active to False"""
        return self.update_agent_status(db=db, agent_id=agent_id, is_active=False)


agent = CRUDAgent(Agent)
