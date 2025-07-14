from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_agent
from app.schemas.agent import Agent, AgentCreate, AgentUpdate
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=Agent, status_code=status.HTTP_201_CREATED)
def create_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_in: AgentCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Agent:
    """
    Create new agent.
    """
    try:
        agent = crud_agent.agent.create(db=db, obj_in=agent_in)
        return agent
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating agent: {str(e)}",
        )


@router.get("/", response_model=List[Agent])
def read_agents(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> List[Agent]:
    """
    Retrieve all agents.
    """
    try:
        agents = crud_agent.agent.get_all_agents(db=db, skip=skip, limit=limit)
        return agents
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching agents: {str(e)}",
        )


@router.get("/active", response_model=List[Agent])
def read_active_agents(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> List[Agent]:
    """
    Retrieve active agents only.
    """
    try:
        agents = crud_agent.agent.get_active_agents(db=db, skip=skip, limit=limit)
        return agents
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active agents: {str(e)}",
        )


@router.get("/{agent_id}", response_model=Agent)
def read_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Agent:
    """
    Get agent by ID.
    """
    agent = crud_agent.agent.get(db=db, id=agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
        )
    return agent


@router.put("/{agent_id}", response_model=Agent)
def update_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_id: int,
    agent_in: AgentUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Agent:
    """
    Update an agent.
    """
    agent = crud_agent.agent.get(db=db, id=agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
        )
    try:
        agent = crud_agent.agent.update(db=db, db_obj=agent, obj_in=agent_in)
        return agent
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating agent: {str(e)}",
        )


@router.delete("/{agent_id}", response_model=Agent)
def delete_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Agent:
    """
    Delete an agent (soft delete - sets is_active to False).
    """
    agent = crud_agent.agent.get(db=db, id=agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
        )
    try:
        agent = crud_agent.agent.delete_agent(db=db, agent_id=agent_id)
        return agent
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting agent: {str(e)}",
        )


@router.get("/name/{agent_name}", response_model=Agent)
def read_agent_by_name(
    *,
    db: Session = Depends(deps.get_db),
    agent_name: str,
    current_user: User = Depends(deps.get_current_user),
) -> Agent:
    """
    Get agent by agent name.
    """
    agent = crud_agent.agent.get_by_agent_name(db=db, agent_name=agent_name)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
        )
    return agent


@router.get("/public/list")
def get_agents_public(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get agents list without authentication (for analytics)
    """
    try:
        agents = crud_agent.agent.get_all_agents(db=db, skip=skip, limit=limit)
        return agents
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching agents: {str(e)}",
        )
