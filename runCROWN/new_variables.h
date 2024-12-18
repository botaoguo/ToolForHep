using namespace ROOT;
#include <Math/Vector4D.h>
#include <Math/VectorUtil.h>
#include <Math/Boost.h>
#include <iostream>
#include <cmath>
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <TVector3.h>

/// function to calculate the lep and mu angle in WH system
///

/// function to calculate W p4
float calc_CosThetaStar_WH_v2(float lepton_pt, float lepton_eta, float lepton_phi,
                              float mu_pt, float mu_eta, float mu_phi) {
    TLorentzVector lepton_vec;
    TLorentzVector mu_vec;
    
    lepton_vec.SetPtEtaPhiM(lepton_pt, lepton_eta, lepton_phi, 0);    
    mu_vec.SetPtEtaPhiM(mu_pt, mu_eta, mu_phi, 0);

    TLorentzVector parent_vec = lepton_vec + mu_vec;
    TVector3 parent_p = parent_vec.BoostVector();
    TVector3 p1,p2;

    lepton_vec.Boost( -parent_p );
    p1 = lepton_vec.BoostVector();

    double cosh_angle = parent_p * p1 / ( parent_p.Mag() * p1.Mag() );
    
    if ( !std::isnan(cosh_angle) && !std::isinf(cosh_angle) ) {
            return cosh_angle;
    } else {
        return -10.0;
    }
}

float calc_CosThetaStar_toWtoH(float W_pt, float W_eta, float W_phi, float W_mass, 
                           float H_pt, float H_eta, float H_phi, float H_mass, 
                           float lepton_pt, float lepton_eta, float lepton_phi,
                           float mu_pt, float mu_eta, float mu_phi) {
    TLorentzVector W_p4;
    TLorentzVector H_p4;
    TLorentzVector lepton_p4;
    TLorentzVector mu_p4;
    W_p4.SetPtEtaPhiM(W_pt, W_eta, W_phi, W_mass);
    H_p4.SetPtEtaPhiM(H_pt, H_eta, H_phi, H_mass);
    lepton_p4.SetPtEtaPhiM(lepton_pt, lepton_eta, lepton_phi, 0);
    mu_p4.SetPtEtaPhiM(mu_pt, mu_eta, mu_phi, 0);
    
    // TLorentzVector TL = W_p4 + H_p4;
    // TVector3 WH_v = TL.Vect();
    
    // TVector3 WHboost = -(TL.BoostVector());    
    // lepton_p4.Boost(WHboost);
    // mu_p4.Boost(WHboost);
    
    TVector3 Wboost = -(W_p4.BoostVector());
    TVector3 Hboost = -(H_p4.BoostVector());
    lepton_p4.Boost(Wboost);
    mu_p4.Boost(Hboost);

    TVector3 lep_v = lepton_p4.Vect();
    TVector3 mu_v = mu_p4.Vect();

    double cosh_angle = ROOT::Math::VectorUtil::CosTheta(lep_v, mu_v);
    
    if ( !std::isnan(cosh_angle) && !std::isinf(cosh_angle) ) {
            return cosh_angle;
    } else {
        return -10.0;
    }
}

float calc_CosThetaStar_toWH(float W_pt, float W_eta, float W_phi, float W_mass, 
                           float H_pt, float H_eta, float H_phi, float H_mass, 
                           float lepton_pt, float lepton_eta, float lepton_phi,
                           float mu_pt, float mu_eta, float mu_phi) {
    TLorentzVector W_p4;
    TLorentzVector H_p4;
    TLorentzVector lepton_p4;
    TLorentzVector mu_p4;
    W_p4.SetPtEtaPhiM(W_pt, W_eta, W_phi, W_mass);
    H_p4.SetPtEtaPhiM(H_pt, H_eta, H_phi, H_mass);
    lepton_p4.SetPtEtaPhiM(lepton_pt, lepton_eta, lepton_phi, 0);
    mu_p4.SetPtEtaPhiM(mu_pt, mu_eta, mu_phi, 0);
    
    TLorentzVector TL = W_p4 + H_p4;
    TVector3 WH_v = TL.Vect();
    
    TVector3 WHboost = -(TL.BoostVector());    
    lepton_p4.Boost(WHboost);
    mu_p4.Boost(WHboost);
    
    // TVector3 Wboost = -(W_p4.BoostVector());
    // TVector3 Hboost = -(H_p4.BoostVector());
    // lepton_p4.Boost(Wboost);
    // mu_p4.Boost(Hboost);

    TVector3 lep_v = lepton_p4.Vect();
    TVector3 mu_v = mu_p4.Vect();

    double cosh_angle = ROOT::Math::VectorUtil::CosTheta(lep_v, mu_v);
    
    if ( !std::isnan(cosh_angle) && !std::isinf(cosh_angle) ) {
            return cosh_angle;
    } else {
        return -10.0;
    }
}

float calc_Weta(float lepton_pt, float lepton_eta, float lepton_phi, float met_pt, float met_phi, float nu_pz) {
    TLorentzVector lepton_p4;
    TLorentzVector nu_p4;
    
    TLorentzVector W_p4;
    
    lepton_p4.SetPtEtaPhiM(lepton_pt, lepton_eta, lepton_phi, 0.0); // Assuming lepton is massless (m = 0)
    float nu_px = met_pt * cos(met_phi);
    float nu_py = met_pt * sin(met_phi);
    float nu_e = sqrt(nu_px * nu_px + nu_py * nu_py + nu_pz * nu_pz);
    nu_p4.SetPxPyPzE(nu_px, nu_py, nu_pz, nu_e);

    W_p4 = lepton_p4 + nu_p4;
    return (float)W_p4.Eta();
}

float calc_Wmass(float lepton_pt, float lepton_eta, float lepton_phi, float met_pt, float met_phi, float nu_pz) {
    TLorentzVector lepton_p4;
    TLorentzVector nu_p4;
    
    TLorentzVector W_p4;
    
    lepton_p4.SetPtEtaPhiM(lepton_pt, lepton_eta, lepton_phi, 0.0); // Assuming lepton is massless (m = 0)
    float nu_px = met_pt * cos(met_phi);
    float nu_py = met_pt * sin(met_phi);
    float nu_e = sqrt(nu_px * nu_px + nu_py * nu_py + nu_pz * nu_pz);
    nu_p4.SetPxPyPzE(nu_px, nu_py, nu_pz, nu_e);

    W_p4 = lepton_p4 + nu_p4;
    return (float)W_p4.M();
}

// Function to calculate neutrino pz solutions using TLorentzVector
float calculateNeutrinoPz(float lepton_pt, float lepton_eta, float lepton_phi, float met_pt, float met_phi, int index) {
    
    const float mW = 80.379; // W boson mass in GeV
    TLorentzVector lepton;
    lepton.SetPtEtaPhiM(lepton_pt, lepton_eta, lepton_phi, 0.0); // Assuming lepton is massless (m = 0)
    // MET (neutrino transverse momentum) components
    float nu_px = met_pt * cos(met_phi);
    float nu_py = met_pt * sin(met_phi);

    // Calculate intermediate values
    float a = (mW * mW) / 2 + lepton.Px() * nu_px + lepton.Py() * nu_py;
    float A = lepton.E() * lepton.E() - lepton.Pz() * lepton.Pz();
    float B = -2 * a * lepton.Pz();
    float C = lepton.E() * lepton.E() * (nu_px * nu_px + nu_py * nu_py) - a * a;

    float discriminant = B * B - 4 * A * C;

    float neutrino_pz1 = 0, neutrino_pz2 = 0;

    if (discriminant < 0) {
        // Complex solution: take real part
        neutrino_pz1 = -B / (2 * A);
        neutrino_pz2 = neutrino_pz1; // Identical since discriminant = 0
    } else {
        // Real solutions
        neutrino_pz1 = (-B + sqrt(discriminant)) / (2 * A);
        neutrino_pz2 = (-B - sqrt(discriminant)) / (2 * A);
    }
    if (index == 0) {
        return neutrino_pz1;
    } else if (index ==1) {
        return neutrino_pz2;
    } else {
        return -10.0f;
    }
    
}

float dphi(float particle1_phi, float particle2_phi) {
    if (particle1_phi - particle2_phi > M_PI) {
        return (float)(particle1_phi - particle2_phi - 2.0*M_PI);
    } else if (particle1_phi - particle2_phi <= - M_PI) {
        return (float)(particle1_phi - particle2_phi + 2.0*M_PI);
    } else {
        return (float)(particle1_phi - particle2_phi);
    }
}
