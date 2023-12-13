use pyo3::prelude::*;
use std::hash::{Hash, Hasher};

#[pyclass]
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum RustRelationships {
    Providers = 1,
    Peers = 2,
    Customers = 3,
    Origin = 4,
    Unknown = 5,
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
    #[pyo3(signature = (prefix, as_path, timestamp, seed_asn, roa_valid_length, roa_origin, recv_relationship, withdraw, traceback_end, communities))]
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
                    // ... handle other fields similarly ...
                    "withdraw" => new_ann.withdraw = value.extract::<bool>(py)?,
                    "traceback_end" => new_ann.traceback_end = value.extract::<bool>(py)?,
                    "communities" => new_ann.communities = value.extract::<Vec<String>>(py)?,
                    _ => return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                        format!("Invalid field name: {}", key),
                    )),
                }
            }
        }

        Ok(new_ann)
    }

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
}

#[pymodule]
fn bgpr(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<RustAnnouncement>()?;
    m.add_class::<RustRelationships>()?;
    Ok(())
}
