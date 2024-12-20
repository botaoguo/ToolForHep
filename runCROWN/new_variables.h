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
float calc_CosThetaStar_WH_v2(float lepton_pt, float lepton_eta, float lepton_phi, float lepton_mass,
                              float mu_pt, float mu_eta, float mu_phi, float mu_mass) {
    TLorentzVector lepton_vec;
    TLorentzVector mu_vec;
    
    lepton_vec.SetPtEtaPhiM(lepton_pt, lepton_eta, lepton_phi, lepton_mass);    
    mu_vec.SetPtEtaPhiM(mu_pt, mu_eta, mu_phi, mu_mass);

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

float calc_CosThetaStar_WH_v1(float lepton_pt, float lepton_eta, float lepton_phi, float lepton_mass,
                              float mu_pt, float mu_eta, float mu_phi, float mu_mass) {
    TLorentzVector lepton_vec;
    TLorentzVector mu_vec;
    
    lepton_vec.SetPtEtaPhiM(lepton_pt, lepton_eta, lepton_phi, lepton_mass);    
    mu_vec.SetPtEtaPhiM(mu_pt, mu_eta, mu_phi, mu_mass);

    TLorentzVector parent_vec = lepton_vec + mu_vec;
    
    TVector3 parent_p = parent_vec.Vect();
    TVector3 parent_boost = -(parent_vec.BoostVector());

    lepton_vec.Boost(parent_boost);
    mu_vec.Boost(parent_boost);
    TVector3 p1 = lepton_vec.Vect();
    TVector3 p2 = mu_vec.Vect();

    float cosh_angle = cos(p1.Angle(parent_p));
    
    if ( !std::isnan(cosh_angle) && !std::isinf(cosh_angle) ) {
            return cosh_angle;
    } else {
        return -10.0;
    }
}

float calc_Weta(float lepton_pt, float lepton_eta, float lepton_phi, float lepton_mass, float met_pt, float met_phi, float nu_pz) {
    TLorentzVector lepton_p4;
    TLorentzVector nu_p4;
    
    TLorentzVector W_p4;
    
    lepton_p4.SetPtEtaPhiM(lepton_pt, lepton_eta, lepton_phi, lepton_mass); 
    float nu_px = met_pt * cos(met_phi);
    float nu_py = met_pt * sin(met_phi);
    float nu_e = sqrt(nu_px * nu_px + nu_py * nu_py + nu_pz * nu_pz);
    nu_p4.SetPxPyPzE(nu_px, nu_py, nu_pz, nu_e);

    W_p4 = lepton_p4 + nu_p4;
    return (float)W_p4.Eta();
}

float calc_Wmass(float lepton_pt, float lepton_eta, float lepton_phi, float lepton_mass, float met_pt, float met_phi, float nu_pz) {
    TLorentzVector lepton_p4;
    TLorentzVector nu_p4;
    
    TLorentzVector W_p4;
    
    lepton_p4.SetPtEtaPhiM(lepton_pt, lepton_eta, lepton_phi, lepton_mass);
    float nu_px = met_pt * cos(met_phi);
    float nu_py = met_pt * sin(met_phi);
    float nu_e = sqrt(nu_px * nu_px + nu_py * nu_py + nu_pz * nu_pz);
    nu_p4.SetPxPyPzE(nu_px, nu_py, nu_pz, nu_e);

    W_p4 = lepton_p4 + nu_p4;
    return (float)W_p4.M();
}

// Function to calculate neutrino pz solutions using TLorentzVector
float calculateNeutrinoPz(float lepton_pt, float lepton_eta, float lepton_phi, float lepton_mass, float met_pt, float met_phi) {
    
    const float mW = 80.379; // W boson mass in GeV
    TLorentzVector lepton;
    lepton.SetPtEtaPhiM(lepton_pt, lepton_eta, lepton_phi, lepton_mass);
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
    if (abs(neutrino_pz1) < abs(neutrino_pz2)) {
        return neutrino_pz1;
    } else {
        return neutrino_pz2;
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

float calculate_ratio(float A, float B) {
    if( B==0 ){
        return -10.0f;
    }else{
        return A/B;
    }
}

float deltaEta(float p1_eta, float p2_eta) {
    return (float)fabs(p1_eta - p2_eta);
}

float scalarPtSum(float pt1, float pt2, float pt3) {
    if (pt1 < 0 || pt2 < 0 || pt3 <0) {
        return -10.0f;
    }
    auto const ptsum = pt1 + pt2 + pt3;
    return (float) ptsum;
}

float calculate_kT(float p1_pt, float p1_eta, float p1_phi, float p1_mass,
                   float p2_pt, float p2_eta, float p2_phi, float p2_mass) {
    if (p1_pt < 0 || p2_pt < 0) {
        return -10.0f;
    }
    TLorentzVector p1_p4,p2_p4;
    p1_p4.SetPtEtaPhiM(p1_pt, p1_eta, p1_phi, p1_mass);
    p2_p4.SetPtEtaPhiM(p2_pt, p2_eta, p2_phi, p2_mass);

    float result = std::min(p1_pt, p2_pt) * ROOT::Math::VectorUtil::DeltaR(p1_p4, p2_p4);
    if ( !std::isnan(result) && !std::isinf(result) ) {
        return result;
    } else {
        return -10.0f;
    }
}

float calculate_antikT(float p1_pt, float p1_eta, float p1_phi, float p1_mass,
                   float p2_pt, float p2_eta, float p2_phi, float p2_mass) {
    if (p1_pt < 0 || p2_pt < 0) {
        return -10.0f;
    }
    TLorentzVector p1_p4,p2_p4;
    p1_p4.SetPtEtaPhiM(p1_pt, p1_eta, p1_phi, p1_mass);
    p2_p4.SetPtEtaPhiM(p2_pt, p2_eta, p2_phi, p2_mass);

    float result = std::min(1.0/p1_pt, 1.0/p2_pt) * ROOT::Math::VectorUtil::DeltaR(p1_p4, p2_p4);
    if ( !std::isnan(result) && !std::isinf(result) ) {
        return result;
    } else {
        return -10.0f;
    }
}
