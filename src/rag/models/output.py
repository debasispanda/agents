from pydantic import BaseModel, Field

class _Citation(BaseModel):
    """One source backing a claim in the answer"""
    file: str = Field(description="Relative path to the markdown file. E.g: '03-incident-2024-q3.md'")
    quote: str = Field(description="Th exact line(s) from the file that supports the claim")
    line_number: int = Field(description="The line number of the quote")

class SearchAnswer(BaseModel):
    """Structured answer with at least once citation per claim."""
    answer: str = Field(description="The answer in plain english.")
    citations: list[_Citation] = Field(description="Files and quotes that support the answer")
