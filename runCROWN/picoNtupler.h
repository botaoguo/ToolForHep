#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
 
using namespace ROOT;
using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
using cRVecF = const ROOT::RVecF &;
using cRVecI = const ROOT::RVecI &;
using cRVecB = const ROOT::RVecB &;
using cRVecC = const ROOT::RVecC &;
using cRVecU = const ROOT::RVecU &;
using cRVecL = const ROOT::RVecL &;

// apply the wz scale
float applyWZscale2018(int is_diboson, int is_WWto2L2Nu, int nele, int nbaseele, int nmuon, int nloosemuon)
{
  // wz
  if (is_diboson == 1 && is_WWto2L2Nu == 0) {
    // m2m or m2m regionc
    if (nmuon == 3 || (nele==0&&nmuon==2&&nloosemuon==3)) {
      return 0.8687175712465628; // TODO
    } else if (nele == 1 || (nele==0&&nbaseele==1&&nmuon==2&&nloosemuon==2)) { // e2m or e2m regionc
      return 0.8323905329630594; // TODO
    } else {
      return 1.0;
    }
  } else {
    return 1.0;
  }
}
// m2m regionb nmuon==3
// m2m regiond nmuon==2 nloosemuon==3
// e2m regionb nele==1
// e2m reigond nele==0 nbaseele==1 nmuon==2 nloosemuon==2
float applyWZscale2022(int is_diboson, int is_WWto2L2Nu, int nele, int nbaseele, int nmuon, int nloosemuon)
{
  // wz
  if (is_diboson == 1 && is_WWto2L2Nu == 0) {
    // m2m or m2m regionc
    if (nmuon == 3 || (nele==0&&nmuon==2&&nloosemuon==3)) {
      return 1.0792;
    } else if (nele == 1 || (nele==0&&nbaseele==1&&nmuon==2&&nloosemuon==2)) { // e2m or e2m regionc
      return 1.0601;
    } else {
      return 1.0;
    }
  } else {
    return 1.0;
  }
}

float applyWZscale2023(int is_diboson, int is_WWto2L2Nu, int nele, int nbaseele, int nmuon, int nloosemuon)
{
  // wz
  if (is_diboson == 1 && is_WWto2L2Nu == 0) {
    // m2m or m2m regionc
    if (nmuon == 3 || (nele==0&&nmuon==2&&nloosemuon==3)) {
      return 1.1323;
    } else if (nele == 1 || (nele==0&&nbaseele==1&&nmuon==2&&nloosemuon==2)) { // e2m or e2m regionc
      return 1.0439;
    } else {
      return 1.0;
    }
  } else {
    return 1.0;
  }
}

float applyDYscale2022(int is_dyjets)
{
  if (is_dyjets == 1) {
    return 1.1; // using pt slice
  } else {
    return 1.0;
  }
}

float applyDYscale2023(int is_dyjets)
{
  if (is_dyjets == 1) {
    return 0.7; // using pt slice
  } else {
    return 1.0;
  }
}