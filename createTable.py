#all table model here
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Numeric, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.jsontools import JsonSerializableBase

#create Base object
Base = declarative_base(cls=(JsonSerializableBase,))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100))

class Species(Base):
    __tablename__ = 'species'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Ensembl(Base):
    __tablename__ = 'ensembl'
    id = Column(Integer, primary_key=True)
    ensembl = Column(String(50), nullable=False, unique=True)
    gene_name = Column(String(50))
    species_id = Column(Integer, ForeignKey('species.id'))
    
class GeneInfo(Base):
    __tablename__ = 'gene_info'
    id = Column(Integer, primary_key=True)
    entrez    = Column(String(50), nullable=False, unique=True)
    symbol  = Column(String(50), nullable=False)
    tax  = Column(Integer)
    mim = Column(String(50))
    hgnc = Column(String(50))
    vega = Column(String(50))
    synonyms     = Column(String(500))
    full_name_from_nomenclature_authority  = Column(String(500))
    locus_tag    = Column(String(50))
    symbol    = Column(String(50))
    ensembl   = Column(String(50))
    chromosome   = Column(String(50))
    description  = Column(String(500))
    feature_type = Column(String(500))
    map_location = Column(String(51))
    type_of_gene = Column(String(50))
    modification_date   = Column(Integer)
    nomenclature_status = Column(String(50))
    symbol_from_nomenclature_authority = Column(String(50))
    species_id = Column(Integer, ForeignKey('species.id'))
     
# class MiM(Base):
#     __tablename__ = 'mim'
#     id = Column(Integer, primary_key=True)
#     mim = Column(Integer, nullable= False)
#     mim_entry_type = Column(String(150), nullable=False)
#     entrez = Column(String(50), nullable=True)
#     gene_name = Column(String(50), nullable=True)
#     ensembl = Column(String(50), nullable=True)
#     
# class GeneAlias(Base):
#     __tablename__ = 'gene_alias'
#     
#     id = Column(Integer, primary_key=True)
#     gene_id = Column(Integer, ForeignKey('gene.id'), nullable=False)
#     alias_name = Column(String(50), nullable=False)
#     

  
class Tissue(Base):
    __tablename__ = 'tissue'
  
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
  
class Scientist(Base):
    __tablename__ = 'scientist'
  
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    scientist_type_id = Column(Integer, ForeignKey('scientist_type.id'))
  
class ScientistType(Base):
    __tablename__ = 'scientist_type'
  
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
  
class ScientistPolicy(Base):
    __tablename__ = 'scientist_policy'
   
    id = Column(Integer, primary_key=True)
    scientist_id = Column(Integer, ForeignKey('scientist.id'), nullable=False)    
    scientist_type_id = Column(Integer, ForeignKey('scientist_type.id'), nullable=False)
   
class Experiment(Base):
    __tablename__ = 'experiment'
   
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    date = Column(DateTime(), nullable=False)
    tech = Column(String(100), nullable=False)
    mim_read_length = Column(Integer, nullable= False)
    species_id = Column(Integer, ForeignKey('species.id'))
    comments = Column(Text)
    scientist_id = Column(Integer, ForeignKey('scientist.id'))
   
class Condition(Base):
    __tablename__ = 'condition'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiment.id'), nullable=False)
  
class Sample(Base):
    __tablename__ = 'sample'
        
    id = Column(Integer, primary_key=True)
    sample_name = Column(String(50), nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiment.id'), nullable=False)
    condition_id = Column(Integer, ForeignKey('condition.id'), nullable=False)
    tissue_id = Column(Integer, ForeignKey('tissue.id'), nullable=False)
    location = Column(String(200), nullable=True)
  
class GeneExpression(Base):
    #raw count gene expression table
    __tablename__ = 'gene_expression_log_rpkm'
    
    id = Column(Integer, primary_key=True)
    ensembl_id = Column(Integer, ForeignKey('ensembl.id'), nullable=False)
    expression = Column(Float, nullable=False)
    sample_id = Column(Integer, ForeignKey('sample.id'), nullable=False)
    # tracking where the gene comes from in a specific file, e.g. creb/creb1
    #file_geneName = Column(String(50))
    
class GeneExpressionRPKM(Base):
    #raw count gene expression table
    __tablename__ = 'gene_expression_rpkm'
    
    id = Column(Integer, primary_key=True)
    ensembl_id = Column(Integer, ForeignKey('ensembl.id'), nullable=False)
    expression = Column(Float, nullable=False)
    sample_id = Column(Integer, ForeignKey('sample.id'), nullable=False)
    # tracking where the gene comes from in a specific file, e.g. creb/creb1
    #file_geneName = Column(String(50))
    
class GeneExpressionTPM(Base):
    #raw count gene expression table
    __tablename__ = 'gene_expression_tpm'
    
    id = Column(Integer, primary_key=True)
    ensembl_id = Column(Integer, ForeignKey('ensembl.id'), nullable=False)
    expression = Column(Float, nullable=False)
    sample_id = Column(Integer, ForeignKey('sample.id'), nullable=False)
    # tracking where the gene comes from in a specific file, e.g. creb/creb1
    #file_geneName = Column(String(50))
   
class DiffGeneExpression(Base):
    __tablename__ = 'diff_gene_expression'
        
    id = Column(Integer, primary_key=True)
    entrez = Column(String(50), nullable=False)
    gene_name = Column(String(50))
    expression = Column(Float)
    experiment_id = Column(Integer, ForeignKey('experiment.id'), nullable=False)
    condition1_id = Column(Integer, ForeignKey('condition.id'), nullable=False)
    condition2_id = Column(Integer, ForeignKey('condition.id'), nullable=False)
    logfc = Column(Float, nullable=False)
    logcpm = Column(Float, nullable=False)
    lr = Column(Float, nullable=False)
    pvalue = Column(Float, nullable=False)
    fdr = Column(Float, nullable=False)
         
class KEGGPathway(Base):
    __tablename__ = 'kegg_pathway'
    
    id = Column(Integer, primary_key=True)
    kegg = Column(String(50), nullable=False)
    description =  Column(String(200))
   
class KeggPathwayGene(Base):
    __tablename__ = 'kegg_pathway_gene'
         
    id = Column(Integer, primary_key=True)
    entrez = Column(String(20), nullable=False)
    pathway_id =  Column(Integer, ForeignKey('kegg_pathway.id'), nullable=False)
   
class KEGGPathwayAnalysis(Base):
    __tablename__ = 'kegg_pathway_analysis'
        
    id = Column(Integer, primary_key=True)
    kegg_pathway_id = Column(Integer, ForeignKey('kegg_pathway.id'), nullable=False)
    description =  Column(String(200))
    n = Column(Integer, nullable=False)
    up = Column(Integer, nullable=False)
    down = Column(Integer, nullable=False)
    p_up = Column(Float, nullable=False)
    fdr_up = Column(Float, nullable=False)
    p_down = Column(Float, nullable=False)
    fdr_down = Column(Float, nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiment.id'), nullable=False)
    condition1_id = Column(Integer, ForeignKey('condition.id'), nullable=False)
    condition2_id = Column(Integer, ForeignKey('condition.id'), nullable=False)
     
class ReactomePathway(Base):
    __tablename__ = 'reactome_pathway'
      
    id = Column(Integer, primary_key=True)
    reactome = Column(String(50), nullable=False)
    description =  Column(String(200))
    species =  Column(String(200))
        
class ReactomePathwayGene(Base):
    __tablename__ = 'reactome_pathway_gene'
         
    id = Column(Integer, primary_key=True)
    entrez = Column(String(20), nullable=False)
    pathway_id =  Column(Integer, ForeignKey('reactome_pathway.id'))
    
   
class ReactomePathwayAnalysis(Base):
    __tablename__ = 'reactome_pathway_analysis'
        
    id = Column(Integer, primary_key=True)
    reactome_id = Column(Integer, ForeignKey('reactome_pathway.id'), nullable=False)
    description =  Column(String(200))
    gene_ratio = Column(String(15), nullable=False)
    bg_ratio = Column(String(15), nullable=False)
    pvalue = Column(Float, nullable=False)
    padjust = Column(Float, nullable=False)
    qvalue = Column(Float)
    genes = Column(String(5000))
    n = Column(Integer, nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiment.id'), nullable=False)
    condition1_id = Column(Integer, ForeignKey('condition.id'), nullable=False)
    condition2_id = Column(Integer, ForeignKey('condition.id'), nullable=False)
     
class Uniprot(Base):
    #this table only contain screted protein
    __tablename__ = 'uniprot'
      
    id = Column(Integer, primary_key=True)
    uniprot = Column(String(50), nullable=False)
    entry_name = Column(String(50))
    protein_name = Column(String(3000))
    length = Column(Integer)
    other_gene_name = Column(String(150))
    species_id = Column(Integer, ForeignKey('species.id'), nullable=False)
    
class Pathview(Base):
    __tablename__ = 'pathview'
    
    id = Column(Integer, primary_key= True)
    kegg_id = Column(Integer, ForeignKey('kegg_pathway.id'), nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiment.id'), nullable=False)
    condition1_id = Column(Integer, ForeignKey('condition.id'), nullable=False)
    condition2_id = Column(Integer, ForeignKey('condition.id'), nullable=False)
    location = Column(String(500))
    
class HumanHomologue(Base):
    __tablename__ = 'human_homologue'
    
    id = Column(Integer, primary_key= True)
    human_ensembl = Column(String(50), nullable=False)
    gene_name = Column(String(50))
    rat_ensembl = Column(String(50))
    human_entrez = Column(String(50))
    mim = Column(String(50))
    symbol = Column(String(50))
    species_id = Column(Integer, ForeignKey('species.id'), nullable=False)

class KEGGDiseasePathway(Base):
    __tablename__ = 'kegg_disease_pathway'
   
    id = Column(Integer, primary_key= True)
    kegg = Column(String(50), nullable=False)
    discription = Column(String(88))
   
class Transporter(Base):
    __tablename__ = 'transporter'
    
    id = Column(Integer, primary_key= True)
    uniprot = Column(String(50))
    other_gene_name = Column(String(72))
    protein_name = Column(String(2000))
    entrez_name = Column(String(50))
    species_id = Column(Integer, ForeignKey('species.id'), nullable=False)

class TranscriptionFactor(Base):
    __tablename__ = 'transcription_factor'
    
    id = Column(Integer, primary_key= True)
    gene_symbol = Column(String(50))
    entrez_human = Column(String(11))
    entrez_rat = Column(String(11))
    entrez_mouse = Column(String(11))
    Uniprot_Human = Column(String(250))
    Uniprot_Rat = Column(String(250))
    Uniprot_mouse = Column(String(250))
    gene_name = Column(String(250))
    synonym = Column(String(128))


