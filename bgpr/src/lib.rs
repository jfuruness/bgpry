use pyo3::prelude::*;
use pyo3::types::PyTuple;
use std::hash::{Hash, Hasher};

#[pyclass]
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum RustRelationships {
    PROVIDERS = 1,
    PEERS = 2,
    CUSTOMERS = 3,
    ORIGIN = 4,
    UNKNOWN = 5,
}
#[pymethods]
impl RustRelationships {
    #[getter]
    fn value(&self) -> i32 {
        *self as i32
    }
    // Add a new associated method to get the name of the enum variant.
    #[getter]
    fn name(&self) -> &str {
        match self {
            RustRelationships::PROVIDERS => "PROVIDERS",
            RustRelationships::PEERS => "PEERS",
            RustRelationships::CUSTOMERS => "CUSTOMERS",
            RustRelationships::ORIGIN => "ORIGIN",
            RustRelationships::UNKNOWN => "UNKNOWN",
        }
    }

    fn __hash__(&self) -> u64 {
        // You can use the value of the enum as its hash
        *self as u64
    }
}


#[pyclass]
#[derive(Clone, Debug)]
pub struct RustAnnouncement {
    prefix: String,
    as_path: Vec<i32>,
    timestamp: i64,
    seed_asn: Option<i32>,
    roa_valid_length: Option<bool>,
    roa_origin: Option<i32>,
    recv_relationship: RustRelationships,
    withdraw: bool,
    traceback_end: bool,
    communities: Vec<String>,
}

#[pymethods]
impl RustAnnouncement {
    #[new]
    #[pyo3(signature = (prefix, as_path, timestamp, seed_asn, roa_valid_length, roa_origin, recv_relationship, withdraw=false, traceback_end=false, communities=Vec::new()))]
    fn new(
        prefix: String,
        as_path: Vec<i32>,
        timestamp: i64,
        seed_asn: Option<i32>,
        roa_valid_length: Option<bool>,
        roa_origin: Option<i32>,
        recv_relationship: RustRelationships,
        withdraw: Option<bool>,
        traceback_end: Option<bool>,
        communities: Option<Vec<String>>,
    ) -> Self {
        RustAnnouncement {
            prefix,
            as_path,
            timestamp,
            seed_asn,
            roa_valid_length,
            roa_origin,
            recv_relationship,
            withdraw: withdraw.unwrap_or(false),
            traceback_end: traceback_end.unwrap_or(false),
            communities: communities.unwrap_or_default(),
        }
    }

    fn prefix_path_attributes_eq(&self, ann: Option<&RustAnnouncement>) -> PyResult<bool> {
        match ann {
            Some(a) => Ok(self.prefix == a.prefix && self.as_path == a.as_path),
            None => Ok(false),
        }
    }

    fn copy(&self, py: Python, overwrite_default_kwargs: Option<std::collections::HashMap<String, PyObject>>) -> PyResult<Self> {
        let mut new_ann = self.clone();

        if let Some(kwargs) = overwrite_default_kwargs {
            for (key, value) in kwargs.iter() {
                match key.as_str() {
                    "prefix" => new_ann.prefix = value.extract::<String>(py)?,
                    "as_path" => new_ann.as_path = value.extract::<Vec<i32>>(py)?,
                    "timestamp" => new_ann.timestamp = value.extract::<i64>(py)?,
                    "seed_asn" => new_ann.seed_asn = value.extract::<Option<i32>>(py)?,
                    "roa_valid_length" => new_ann.roa_valid_length = value.extract::<Option<bool>>(py)?,
                    "roa_origin" => new_ann.roa_origin = value.extract::<Option<i32>>(py)?,
                    "recv_relationship" => new_ann.recv_relationship = value.extract::<RustRelationships>(py)?,
                    "withdraw" => new_ann.withdraw = value.extract::<bool>(py)?,
                    "traceback_end" => new_ann.traceback_end = value.extract::<bool>(py)?,
                    "communities" => new_ann.communities = value.extract::<Vec<String>>(py)?,
                    _ => return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                        format!("Field not found in RustAnnouncement: {}", key),
                    )),
                }
            }
        }

        Ok(new_ann)
    }
    // Every attr needs a getter to be able to be used in Python
    #[getter]
    fn prefix(&self) -> &str {
        &self.prefix
    }

    //#[getter]
    //fn as_path(&self) -> Vec<i32> {
    //    self.as_path.to_owned()
    //}

    #[getter]
    fn as_path(&self, py: Python) -> Py<PyTuple> {
        // Convert Vec<i32> to PyTuple
        PyTuple::new(py, &self.as_path).into()
    }

    #[getter]
    fn timestamp(&self) -> i64 {
        self.timestamp
    }

    #[getter]
    fn seed_asn(&self) -> Option<i32> {
        self.seed_asn
    }

    #[getter]
    fn roa_valid_length(&self) -> Option<bool> {
        self.roa_valid_length
    }

    #[getter]
    fn roa_origin(&self) -> Option<i32> {
        self.roa_origin
    }

    #[getter]
    fn recv_relationship(&self) -> RustRelationships {
        self.recv_relationship
    }

    #[getter]
    fn withdraw(&self) -> bool {
        self.withdraw
    }

    #[getter]
    fn traceback_end(&self) -> bool {
        self.traceback_end
    }

    //#[getter]
    //fn communities(&self) -> Vec<String> {
    //    self.communities.to_owned()
    //}
    #[getter]
    fn communities(&self, py: Python) -> Py<PyTuple> {
        // Convert Vec<String> to PyTuple
        PyTuple::new(py, &self.communities).into()
    }

    // Properties below
    #[getter]
    fn invalid_by_roa(&self) -> PyResult<bool> {
        Ok(match self.roa_origin {
            Some(roa_origin) => self.origin() != roa_origin || !self.roa_valid_length.unwrap_or(false),
            None => false,
        })
    }

    #[getter]
    fn valid_by_roa(&self) -> PyResult<bool> {
        Ok(self.roa_origin == Some(self.origin()) && self.roa_valid_length.unwrap_or(false))
    }

    #[getter]
    fn unknown_by_roa(&self) -> PyResult<bool> {
        Ok(!self.invalid_by_roa()? && !self.valid_by_roa()?)
    }

    #[getter]
    fn covered_by_roa(&self) -> PyResult<bool> {
        Ok(!self.unknown_by_roa()?)
    }

    #[getter]
    fn roa_routed(&self) -> PyResult<bool> {
        Ok(self.roa_origin.unwrap_or(0) != 0)
    }

    fn origin(&self) -> i32 {
        *self.as_path.last().unwrap_or(&0)
    }

    fn __str__(&self) -> PyResult<String> {
        Ok(format!("{} {:?} {:?}", self.prefix, self.as_path, self.recv_relationship))
    }

    fn __hash__(&self) -> PyResult<u64> {
        let mut hasher = std::collections::hash_map::DefaultHasher::new();
        self.__str__()?.hash(&mut hasher);
        Ok(hasher.finish())
    }

    // For pickling
    fn __getstate__(&self) -> PyResult<(String, Vec<i32>, i64, Option<i32>, Option<bool>, Option<i32>, RustRelationships, bool, bool, Vec<String>)> {
        Ok((
            self.prefix.clone(),
            self.as_path.clone(),
            self.timestamp,
            self.seed_asn,
            self.roa_valid_length,
            self.roa_origin,
            self.recv_relationship,
            self.withdraw,
            self.traceback_end,
            self.communities.clone(),
        ))
    }

    // Custom deserialization method
    fn __setstate__(&mut self, py: Python, state: &PyAny) -> PyResult<()> {
        let state_tuple: &PyTuple = state.extract()?;

        if state_tuple.len() != 10 {
            return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                "Invalid state length".to_string()
            ));
        }
        self.prefix = state_tuple.get_item(0)?.extract::<String>()?;
        self.as_path = state_tuple.get_item(1)?.extract::<Vec<i32>>()?;
        self.timestamp = state_tuple.get_item(2)?.extract::<i64>()?;
        self.seed_asn = state_tuple.get_item(3)?.extract::<Option<i32>>()?;
        self.roa_valid_length = state_tuple.get_item(4)?.extract::<Option<bool>>()?;
        self.roa_origin = state_tuple.get_item(5)?.extract::<Option<i32>>()?;
        self.recv_relationship = state_tuple.get_item(6)?.extract::<RustRelationships>()?;
        self.withdraw = state_tuple.get_item(7)?.extract::<bool>()?;
        self.traceback_end = state_tuple.get_item(8)?.extract::<bool>()?;
        self.communities = state_tuple.get_item(9)?.extract::<Vec<String>>()?;

        Ok(())
    }
}

#[pymodule]
fn bgpr(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<RustAnnouncement>()?;
    m.add_class::<RustRelationships>()?;
    Ok(())
}
